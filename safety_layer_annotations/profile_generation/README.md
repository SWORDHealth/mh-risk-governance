# Prompts used to build the synthetic patient profiles

These are the LLM prompts behind the patient profiles that drove the 662
conversations.

```
profile_generation/
├── README.md
├── backstory_generation/        Backstory generation: one prompt per scenario category
│   ├── no_crisis.txt
│   ├── victim.txt
│   └── perpetrator.txt
└── profile_generation/          Profile generation
    ├── layer_1.txt              Layer 1 · Infer
    └── layer_3.txt              Layer 3 · Contextualize
```

## Pipeline (as in Supplementary Figure 1 of the paper)

1. **Backstory generation** (`backstory_generation/`). Each CRADLE Bench
   narrative (a first-person Reddit post with its risk labels) is rewritten
   into a short second-person *session scenario* and a *session goal*: what
   is on the patient's mind when they open the chat, and what they want from
   it. The prompt is chosen by scenario category; `{post}` and `{labels}`
   are filled with the narrative and its labels (from CRADLE dataset).
2. **Layer 1 · Infer** (`layer_1.txt`). An LLM reads the
   scenario and the original narrative and *pins* only the profile
   attributes the text actually evidences (e.g. gender, employment,
   relationship status, symptom severity), plus, for self-harm scenarios,
   suicide risk factors, warning signs and protective factors. Everything
   else is left unset.
3. **Layer 2 · Enrich** (deterministic, no prompt). Pinned attributes are
   propagated to dependent fields, and the remaining unpinned attributes are
   filled by stratified sampling against population targets. The attribute names and
   allowed values referenced in `layer_1.txt` are the ones sampled here.
4. **Layer 3 · Contextualize** (`layer_3.txt`). An LLM writes a two-paragraph
   background that integrates the attributes into a coherent person. The
   scenario, goal and (where applicable) the original narrative are appended
   to this prompt as steering context.

## Terms used in the prompts

**Scenario category ("voice").** The prompts name the three categories by
the role of the patient rather than by risk type:

| in the prompts | in the paper | CRADLE Bench label categories | source narratives |
|---|---|---|---|
| `no_crisis` | safe | `no_crisis` | posts with no crisis content |
| `victim` | self-harm | `suicideideation_*`, `selfharm_*` | the patient is the person at risk, as in the post |
| `perpetrator` | harm-to-others | `domesticviolence_*`, `rape_*`, `sexualharassment_*`, `childabuse_endangerment_*` | these posts are written by the person harmed; the prompt **flips the account to the perspective of the person doing the harm**, so that the patient is the one expressing intent or describing their own behaviour |

The `_*` suffix carries CRADLE's temporal tag (`ongoing` / `past`) and, for
suicidal ideation, severity (`active` / `passive`); the backstory prompts use
these for calibration. Items whose labels span more than one category were
excluded.

The flip is necessary because CRADLE Bench contains no first-person
harm-to-others narratives.

**Disclosure variant (`direct` / `layered`).** Every scenario is generated
in two versions from the same narrative, and both are used:

- `direct`: the patient opens the session with the issue.
- `layered`: the patient opens with surface framing (mood, frustration,
  something being off); the underlying issue is disclosed only when the
  conversation gets there.

This is a diversity device. It doubles the number of distinct scenarios per
narrative and spreads risk disclosure across explicit, indirect and
progressive patterns, so the safety layer is tested on early, late and
gradual onsets rather than on one disclosure style. In the released data
the variant is given per conversation in `disclosure_variant`.

**Profile attributes.** A profile has several dozen demographic, social,
lifestyle and clinical fields. `layer_1.txt` lists the ones an LLM may pin
and their allowed values; `layer_3.txt` shows the full set as `$field`
placeholders in the order they are rendered.

**Archetype.** A stable conversational posture assigned to each patient
(e.g. minimizer, intellectualizer). Layer 1 only blocks archetypes that
would be incoherent with the scenario; the assignment itself happens in
Layer 2.

## Notes

- `layer_1.txt` is the prompt exactly as rendered, with the option lists
  expanded.
- `layer_3.txt` is a template; `$name`, `$age`, … are substituted per
  profile.
- Prompts were run once per narrative, and the resulting profiles were
  fixed before any conversation was generated.
