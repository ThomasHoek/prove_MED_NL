# Issues fixed and found locally during testing

## prove_SICK_NL/prolog/lassy.pl

```
lassyTagFeatList2Penn(['vnw'-Feats], POS) :-
    ( subset(['betr'], Feats) -> POS = 'WDT'  % WP?
    ; subset(['bez'],  Feats) -> POS = 'PRP$'
    ; subset(['onbep'],Feats) -> POS = 'DT'
    ; subset(['aanw'], Feats) -> POS = 'EX'
    ; subset(['recip'],Feats) -> POS = 'DT'
    ; subset(['refl'], Feats) -> POS = 'PRP'
    ; subset(['pers'],  Feats) -> POS = 'PRP'   % added
    ; subset(['per'],  Feats) -> POS = 'PRP'    % can be removed?
    ; subset(['pr'],  Feats) -> POS = 'PRP'     % added
    ; subset(['vb'],   Feats) -> POS = 'WP'
    ).
```

The bold line was added, the alpino.json results are PERS, not PER.
Does add bugs for problems though; to be tested.
These files are in: MED_NL/problems/

## FOUND; %problem id = 134, 1008 | unknown type cp -> [dat, als, dan] | Complementizer phrase
[Complementizer phrase](https://www.ucl.ac.uk/dutchstudies/an/SP_LINKS_UCL_POPUP/SPs_english/linguistics/glossary_c.html) (CP) - a functional phrase in sentences. Named so because it often contains a complementizer (that).

sen_id(908, 134, 'p', 'crowd', 'unknown', 'Een paar mensen zeggen dat dertien een ongeluksgetal is.').
Error during parsing tlg_term_to_ttterm.

% TLG Simple type to CCG simple type
simple_tlg_to_ccg(A~>B, X~>Y) :- !,
    simple_tlg_to_ccg(A, X),
    simple_tlg_to_ccg(B, Y).

A~>B is a single Atom ???

Fix; add as exception rule for 'cp' labels??
```
% thomas testing
simple_tlg_to_ccg(cp, cp).
```



## 470 [alles behalve] breaks the parser

sen_id(2287, 470, 'p', 'crowd', 'unknown', 'Ik ben alles behalve een leugenaar.').

1. [alles] [behalve] -> merges into alles_behalve
2. new type ->  'VNW(onbep,pron,stan,vol,3o,ev)_VG(onder)'
3. correct splt in l_postag    ['VNW(onbep,pron,stan,vol,3o,ev)','VG(onder)']
4. cleaned into L_PrologTerm [vnw(onbep,pron,stan,vol,'3o',ev),vg(onder)]
5. second clearn L_Tag_Feats   [vnw-[onbep, pron, stan, vol, '3o', ev], vg-[onder]]
6. ???
7. maplist([TagF, P]>>lassyTagFeatList2Penn([TagF], P), L_Tag_Feats, L_Pos), \
8. vnw ends up in `lassyTagFeatList2Penn` and errors. \
9. function fails. 


## sv1? -> fix into main:dcl ??
sv1	verb-initial sentence (yes/no question, imperatives)
```
simple_tlg_to_ccg(sv1, s:dlc).
```

## Aethel eats away words  -> MED_NL/problems/broken_alpino_aethel_sent_debug.txt
4558.xml -> <sentence sentid="4558">Vandaag is niet goed voor mij .</sentence> \
alpino_aethel.pl: sen_id_tlg_tok(4558, \
((t(1,(sv1) ~> (sv1))) @ (((t(0,(adjp) ~> (sv1))) @ (((t(2,(pp) ~> (adjp))) @ (((t(3,(vnw) ~> (pp))) @ (t(4,vnw))))))))),\
[['is'], ['niet'], ['goed'], ['voor'], ['mij'], ['.']]\
).

Vandaag gone?!

Aethel also merges words? Intended??