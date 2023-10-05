# Wordnet and LLFs

## wordnet
### problem: 3834

this does not fix it?
```

% assertz(s('TH-0', _, 'kippeneieren', 'n', 1, _)),
% assertz(s('TH-1', _, 'kip_ei', 'n', 1, _)),

% assertz(hyp('eng-30-01460457-n', 'TH-0')),	
% assertz(hyp('TH-0', 'eng-30-01460457-n')),	
% assertz(hyp('eng-30-01460457-n', 'TH-1')),	
% assertz(hyp('TH-1', 'eng-30-01460457-n')),	
```


### problem 1276

rijsbier -> biertje?
cant add relation to WN?
```
% assertz(s('TH-0', _, 'rijstbier', 'n', 1, _)),
% assertz(s('TH-1', _, 'rijst bier', 'n', 1, _)),
% assertz(hyp('eng-30-07886849-n', 'TH-0')),	
% assertz(hyp('eng-30-07886849-n', 'TH-1')),	
```


### problem 350
dieselbus -> diesel 
cant add relation


---------

## LLFs?

Can't generate LLF xml using produce? \
Bugged due to no CCG but using other? \
https://github.com/kovvalsky/LangPro/wiki/Producing-LLFs

```bash
?- parList([html, parts([crowd])]), xml_probs_llfs(_, 'My_LLFs').
True
```
However\

```xml
XML/myLLFs.xml
<parsed_problems>
<parsed_problem probID="500">
<parsed_sentence>
<id_sent>P<sub>1042</sub>: Er liggen een paar sinaasappels op de tafel.</id_sent>
Warning: Sentence could not be parsed

</parsed_sentence>
<parsed_sentence>
<id_sent>H<sub>1043</sub>: Er liggen een paar versgeplukte sinaasappels op de tafel.</id_sent>
Warning: Sentence could not be parsed
</parsed_sentence>
</parsed_problem>
```


### 1706 [sent: 2627] -> helemaal@not not recognised as a negative?
helemaal@not@(X) ->[should be] helemaal@(not@(X))


### 3418 [sent: 1916] -> nooit
Nooit is not recognised as: "not once"/ "not ever" / "not"

### 1348 -> Geen | BIG ISSUE
Geen gets mapped to nearest noun\
geen mooie zus -> a@(mooi@(no@zus))\
geen zus -> a@((no@zus)) 

ERROR: mooi@(no@zus) == no@zus \
fix? no@(mooi@zus) != (no@zus)

Also incorrect application of monotonocity raising when its negated, eg geen.
