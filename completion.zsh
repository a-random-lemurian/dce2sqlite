#compdef dce2sqlite

_dce2sqlite() {
    local I="-h --help --version"
    local ret=1
    local -a args

    args+=(
        "($I ):file:_files"
        "($I -o --output)"{-o+,--output=}'[Path to output file]:file:_files'
        '(-*)'{-i,--input}'[Input file]:file:_files'
        '(-*)'{-h,--help}'[Print help message and exit]'
        '(-*)'{-a,--append}'[Append to an already-existing database]'
        '(-*)'{-i,--index}'[Create an index on the database]'
    )

    _arguments -w -s -S $args[@] && ret=

    return ret
}

compdef _dce2sqlite dce2sqlite
