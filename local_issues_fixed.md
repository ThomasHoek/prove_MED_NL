# Issues fixed and found locally during testing

## prove_SICK_NL/prolog/lassy.pl

lassyTagFeatList2Penn(['vnw'-Feats], POS) :-
    ( subset(['betr'], Feats) -> POS = 'WDT'  % WP?
    ; subset(['bez'],  Feats) -> POS = 'PRP$'
    ; subset(['onbep'],Feats) -> POS = 'DT'
    ; subset(['aanw'], Feats) -> POS = 'EX'
    ; subset(['recip'],Feats) -> POS = 'DT'
    ; subset(['refl'], Feats) -> POS = 'PRP'
    **; subset(['pers'],  Feats) -> POS = 'PRP_**
    ; subset(['per'],  Feats) -> POS = 'PRP'
    **; subset(['pr'],  Feats) -> POS = 'PRP'**
    ; subset(['vb'],   Feats) -> POS = 'WP'
    ).

The bold line was added, the alpino.json results are PERS, not PER.
Does add bugs for problems though; to be tested.
These files are in: MED_NL/problems/


# FOUND; %problem id = 134
sen_id(908, 134, 'p', 'crowd', 'unknown', 'Een paar mensen zeggen dat dertien een ongeluksgetal is.').
Error during parsing tlg_term_to_ttterm.

% TLG Simple type to CCG simple type
simple_tlg_to_ccg(A~>B, X~>Y) :- !,
    simple_tlg_to_ccg(A, X),
    simple_tlg_to_ccg(B, Y).

A~>B is a single Atom ???

Fix; add as exception rule for 'cp' labels??
