%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
:- ensure_loaded([
	'wn_hyp',
	%'wn_h_',
 	'wn_sim',
	'wn_ant',
	'wn_der',
	'wn_s'
	]).

:- dynamic s/6.
:- dynamic hyp/2.


odwn_patch :-
	retractall(s('eng-30-00007846-n', _, 'man', 'n', 3, _)),
	% assertz(s('TH-0', _, 'kippeneieren', 'n', 1, _)),
	% assertz(s('TH-1', _, 'kip_ei', 'n', 1, _)),

	% assertz(hyp('eng-30-01460457-n', 'TH-0')),	
	% assertz(hyp('TH-0', 'eng-30-01460457-n')),	
	% assertz(hyp('eng-30-01460457-n', 'TH-1')),	
	% assertz(hyp('TH-1', 'eng-30-01460457-n')),	


	% assertz(hyp('eng-30-07886849-n', 'TH-0')),	
	% assertz(hyp('eng-30-07886849-n', 'TH-1')),	
	assertz(hyp('eng-30-13104059-n', 'eng-30-12212361-n')).

% block certain unwanted senses
:- odwn_patch.

% 	assertz(s('TH-0', _, 'dieselbus', 'n', 1, _)),	
	% assertz(hyp('eng-30-02924116-n', 'TH-0')),
	