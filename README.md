# prove_MED_NL

Prove Dutch NLI problems of [MED-NL](https://aclanthology.org/2023.findings-eacl.110/) with [LangPro](https://github.com/kovvalsky/LangPro) by modifying a [prover](https://github.com/kovvalsky/prove_SICK_NL) made for [SICK-NL](https://github.com/gijswijnholds/sick_nl).

## Prerequisites

1. In `config.txt`, set the path to [LangPro](https://github.com/kovvalsky/LangPro) and to [prove_SICK_NL](https://github.com/kovvalsky/prove_SICK_NL).
   - Or place all three folders in the same parent folder for automatic configuration.
   - Incase you want to replicate the results on MED, change the WN location to LangPro/WNProlog

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

5. Certain lines are currently broken and will cause the entail_all to stop; the broken lines are in MED_NL/problems/sen_pl_prob.txt.
   These sentences are currently commented out in sen.pl, but if you want to replicate you have to comment these back unless they are fixed.

## Running
Please check the `solve_sick` folder and `langpro` repo's for instructions, below is a summerisation of how to use produce commands specifically for this repo. For the results, please use the produce.ini file.

---

Multiple produce commands have been setup to ease up the use of testing. To manually load langpro, you can use one of the following commands:

## Dutch MED

This is the standard command used to test with LangPro, this preloads already working settings and allows for easy testing.
```bash
produce langpro_crowd_alpino
```
or
```bash
produce langpro_paper_alpino
```

These are commands to load a pure langpro parser un-initialised, you will receive an echo with a "ready to go" command which can be modified.
```bash
produce langpro_MEDNL_paper
```
or
```bash
produce langpro_MEDNL_crowd
```


## English
For the English MED, seperate commands were created due to discrepacy in pathing and commands. The pure command for this is

```bash
produce langpro_MED_paper
```
or
```bash
produce langpro_MED_crowd
```
