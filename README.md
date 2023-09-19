# prove_MED_NL

Prove Dutch NLI problems of [MED-NL](https://aclanthology.org/2023.findings-eacl.110/) with [LangPro](https://github.com/kovvalsky/LangPro) by modifying a [prover](https://github.com/kovvalsky/prove_SICK_NL) made for [SICK-NL](https://github.com/gijswijnholds/sick_nl).

## Prerequisites

1. In `config.txt`, set the path to [LangPro](https://github.com/kovvalsky/LangPro) and to   [prove_SICK_NL](https://github.com/kovvalsky/prove_SICK_NL).
   - Or place all three folders in the same parent folder for automatic configuration.

2. Get Langpro repo with
`git clone --branch nl git@github.com:kovvalsky/LangPro.git` or `git clone --branch nl https://github.com/kovvalsky/LangPro.git`.
It is used for theorem-proving and converting type-logical terms into simply-typed terms.
Note that `nl` branch is relevant one.
Additionally add `--single-branch` if you want to clone only `nl` branch.

3. (ONLY FOR REPRODUCTION) Please download the [aethel](https://github.com/konstantinosKokos/aethel/tree/dev) repo (dev branch) and place it inside the solve_MED repo.
`git clone --branch dev https://github.com/konstantinosKokos/aethel.git`
After this run `produce fix_aethel` or manually replace the following lines in `aethel/script/langpro_interface`:
   - `return f'v(X{index},{type_to_natlog(_type)}'` ->
    `return f'v(X{index},{type_to_natlog(_type)})'`
     - The step above added a `)` at the end.
   - `return f'(abst({term_to_natlog(var)},{term_to_natlog(body)}))'` ->
      `return f'abst({term_to_natlog(var)},{term_to_natlog(body)})'`
     - The step above removes the outer brackets.

4. `produce.ini` contains rules how to generate files.
You will need to install [produce](https://github.com/texttheater/produce) if you want to use the rules to build files from scratch.

5. (TEMP FIX): Certain lines are currently broken; please comment all sentences in `%problem id = 97` and `%problem id = 98` in sen.pl

## Running

Please check the `solve_sick` folder and `langpro` folder for instructions.
Future tutorial and helpful commands to be added soon.

---

```bash
#  loading the prover with alpino (or npn_robbert) trees
produce langpro
```

```prolog
% This can be run only in the beginning, to set the global parameters: the part of the dataset, language flag, lexical annotation file, and theorem proving parameters
parList([parts([paper]), lang(nl), anno_json('MED_NL/anno/alpino.json'), complete_tree, allInt, aall, wn_ant, wn_sim, wn_der, constchck]).
parList([parts([crowd]), lang(nl), anno_json('MED_NL/anno/alpino.json'), complete_tree, allInt, aall, wn_ant, wn_sim, wn_der, constchck]).

parList([parts([paper]), lang(nl), anno_json('MED_NL/anno/alpino.json'), complete_tree, allInt, aall, wn_ant, wn_sim, wn_der, constchck, waif('Results/result.txt')]).
parList([parts([crowd]), lang(nl), anno_json('MED_NL/anno/alpino.json'), complete_tree, allInt, aall, wn_ant, wn_sim, wn_der, constchck, waif('Results/result.txt')]).

parList([parts([paper]), parallel(X), lang(nl), anno_json('MED_NL/anno/alpino.json'), complete_tree, allInt, aall, wn_ant, wn_sim, wn_der, constchck, waif('Results/result.txt')]).
parList([parts([crowd]), parallel(X), lang(nl), anno_json('MED_NL/anno/alpino.json'), complete_tree, allInt, aall, wn_ant, wn_sim, wn_der, constchck, waif('Results/result.txt')]).
```
