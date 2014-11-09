# Sublime Semicolon plugin

Add semicolons automatically by hotkey.

### Demo

![Demo](https://github.com/shagabutdinov/sublime-enhanced-demos/raw/master/semicolon.gif "Demo")


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Features

1. Add semicolon at the end of current statement.

2. Add semicolon where linter tells it should be.

Not that you have to have sublime-linter activated for language you write if you
want to use "add all semicolons". Plugin was tested with php/javascript linters
and likely will fail to work with other. If it'll happen please open an issue
and make a pull request if you are able to fix it manually.

### Usage

Hit keyboard shortcut to add semicolon.

Example:

  ```
  # before
  alert('Missing semicolon|') # <- cursor here

  # after "add semicolon at the end of current statement"
  alert('Missing semicolon');

  # before
  call1|(); # <- cursor here
  call2();
  alert('Missing semicolon')

  # after "add semicolon by linter message"
  call1();
  call2();
  alert('Missing semicolon');
  ```


### Commands

| Description       | Keyboard shortcut | Command palette           |
|-------------------|-------------------|---------------------------|
| Add semicolon     | alt+w             | Semicolon: Add            |
| Add semicolons    | alt+shift+w       | Semicolon: Add everywhere |


### Dependencies

* [Statement](https://github.com/shagabutdinov/sublime-statement)
* https://github.com/SublimeLinter/SublimeLinter3
* https://github.com/SublimeLinter/SublimeLinter-[your language]