# Issues fixed and found locally during testing

## prove_SICK_NL/prolog/lassy.pl

lassyTagFeatList2Penn(['vnw'-Feats], POS) :-
    ( subset(['betr'], Feats) -> POS = 'WDT'  % WP?
    ; subset(['bez'],  Feats) -> POS = 'PRP$'
    ; subset(['onbep'],Feats) -> POS = 'DT'
    ; subset(['aanw'], Feats) -> POS = 'EX'
    ; subset(['recip'],Feats) -> POS = 'DT'
    ; subset(['refl'], Feats) -> POS = 'PRP'
    **; subset(['pers'],  Feats) -> POS = 'PRP'**
    ; subset(['per'],  Feats) -> POS = 'PRP'
    **; subset(['pr'],  Feats) -> POS = 'PRP'**
    ; subset(['vb'],   Feats) -> POS = 'WP'
    ).

The bold line was added, the alpino.json results are PERS, not PER.
Does add bugs for problems though; to be tested.
These files are in: MED_NL/problems/

## FOUND; %problem id = 134, 1008 | unknown type cp

sen_id(908, 134, 'p', 'crowd', 'unknown', 'Een paar mensen zeggen dat dertien een ongeluksgetal is.').
Error during parsing tlg_term_to_ttterm.

% TLG Simple type to CCG simple type
simple_tlg_to_ccg(A~>B, X~>Y) :- !,
    simple_tlg_to_ccg(A, X),
    simple_tlg_to_ccg(B, Y).

A~>B is a single Atom ???

Fix; add as exception rule for 'cp' labels??

## 470 [alles behalve] breaks the parser

sen_id(2287, 470, 'p', 'crowd', 'unknown', 'Ik ben alles behalve een leugenaar.').

[alles] [behalve] -> merges into alles_behalve
new type ->  'VNW(onbep,pron,stan,vol,3o,ev)_VG(onder)'
correct splt in l_postag    ['VNW(onbep,pron,stan,vol,3o,ev)','VG(onder)']
cleaned into L_PrologTerm [vnw(onbep,pron,stan,vol,'3o',ev),vg(onder)]
second clearn L_Tag_Feats   [vnw-[onbep, pron, stan, vol, '3o', ev], vg-[onder]]
???
maplist([TagF, P]>>lassyTagFeatList2Penn([TagF], P), L_Tag_Feats, L_Pos),
vnw ends up in `lassyTagFeatList2Penn` and errors.
function fails.
