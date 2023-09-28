# Issues fixed locally during testing

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
    ; subset(['vb'],   Feats) -> POS = 'WP'
    ).

The bold line was added, the alpino.json results are PERS, not PER.
Does add bugs for problems though; to be tested.
These files are in: MED_NL/problems/