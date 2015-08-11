import sublime
import sublime_plugin
import re

from Statement import statement
from Expression import expression

try:
  from SublimeLinter.lint import persist
except ImportError:
  sublime.error_message("Dependency import failed; please read readme for " +
   "Statement plugin for installation instructions; to disable this " +
   "message remove this plugin")


def add(view, edit, point):
  container = statement.get_root_statement(view, point)
  line = view.line(container[1])

  next_char = view.substr(sublime.Region(line.b, line.b + 1))

  prev_char_region = sublime.Region(line.a, line.b)
  prev_chars = view.substr(prev_char_region)
  prev_char_match = re.search(r'(\S)\s*$', prev_chars)

  prev_char = None
  if prev_char_match != None:
    prev_char = prev_char_match.group(1)

  is_semicolon_not_required = (
    prev_char == ';' or
    prev_char == ':' or
    prev_char == ',' or
    next_char == ';'
  )

  is_source = (
    'source' not in view.scope_name(line.b) or
    'source' not in view.scope_name(line.b + 1)
  )

  if is_source:
    is_semicolon_not_required = True

  is_keyword = is_keyword_statement(view, line.a + prev_char_match.start(1) + 1)
  if prev_char == '}' and is_keyword:
    is_semicolon_not_required = True

  if is_semicolon_not_required:
    return

  view.insert(edit, container[1], ';')
  new_sels = []
  for current_sel in view.sel():
    a, b = current_sel.a, current_sel.b

    if a - 1 == container[1]:
      a -= 1

    if b - 1 == container[1]:
      b -= 1

    new_sels.append(sublime.Region(a, b))

  view.sel().clear()
  view.sel().add_all(new_sels)

def is_keyword_statement(view, point):
  nesting = expression.get_nesting(view, point - 1, expression = r'{')
  if nesting == None:
    return False

  chars_before_nesting = view.substr(sublime.Region(
    max(nesting[0] - 512, 0),
    nesting[0] - 1
  ))

  match = re.search(r'\)(\s*)$', chars_before_nesting)
  if match == None:
    return False

  parenthesis_nesting = expression.get_nesting(view, nesting[0] - 2 -
    len(match.group(1)), expression = r'\(')

  if parenthesis_nesting == None:
    return False

  chars_before_parenthesis = view.substr(sublime.Region(
    max(parenthesis_nesting[0] - 512, 0),
    parenthesis_nesting[0] - 1
  ))

  keyword_regexp = r'(if|for|while|function\s+\w+)\s*$'
  return re.search(keyword_regexp, chars_before_parenthesis) != None

def add_all(view, edit):
  if not view.id() in persist.errors:
    return

  errors = persist.errors[view.id()]
  for line in errors:
    for error in errors[line]:
      position, error_text = error

      point = view.text_point(line, position) - 1
      is_semicolon_required = (
        'unexpected' in error_text or
        'Missing semicolon' in error_text or
        'missing semicolon' in error_text
      )

      if is_semicolon_required:
        _add(view, edit, point)

def _add(view, edit, point):
  statement_start = view.line(point).a
  statement_point = _get_previous_statement_point(view, statement_start)

  add(view, edit, statement_point)

def _get_previous_statement_point(view, point):
  while True:
    if point <= 0:
      return None

    line = view.line(point)
    point = line.a - 1
    text = view.substr(line)
    if text.strip() == '':
      continue

    scope_a_point = line.a + len(text) - len(text.lstrip())
    scope_a = view.scope_name(scope_a_point)
    scope_b = view.scope_name(line.b - 1)
    if 'comment' in scope_b:
      if 'comment' in scope_a:
        continue
      else:
        return scope_a_point

    return line.b