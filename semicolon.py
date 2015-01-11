import sublime
import sublime_plugin

from Statement import statement

try:
  from SublimeLinter.lint import persist
except ImportError:
  sublime.error_message("Dependency import failed; please read readme for " +
   "Statement plugin for installation instructions; to disable this " +
   "message remove this plugin")


def add(view, edit, point):
  container = statement.get_root_statement(view, point)
  line = view.line(container[1])
  last_char_region = sublime.Region(line.b - 1, line.b)
  last_char = view.substr(last_char_region)

  if last_char == ';' or last_char == ':' or last_char == ',':
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

def add_all(view, edit):
  if not view.id() in persist.errors:
    return

  errors = persist.errors[view.id()]
  for line in errors:
    for error in errors[line]:
      position, error_text = error

      point = view.text_point(line, position)
      is_semicolon_required = False

      # php and jshint
      if 'unexpected' in error_text or 'Missing semicolon' in error_text:
        is_semicolon_required = True
        point -= 1

      # jsl
      if 'missing semicolon' in error_text:
        is_semicolon_required = True

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