def term_to_natlog(term: Term) -> str:
    match term:
        case Variable(_type, index):
            return f'v(X{index},{type_to_natlog(_type)})'
        case Constant(_type, index):
            return f't({index},{type_to_natlog(_type)})'
        case ArrowElimination(function, argument):
            return f'(({term_to_natlog(function)}) @ ({term_to_natlog(argument)}))'
        case ArrowIntroduction(var, body):
            return f'(abst({term_to_natlog(var)},{term_to_natlog(body)}))'
        case _:
            raise ValueError(f'Unexpected term constructor: {type(term)}')
