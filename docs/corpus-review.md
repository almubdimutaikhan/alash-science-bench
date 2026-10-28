# Alash scholarly knowledge benchmark: corpus review

Reviewed on 25 October 2026. Source folder: `drive-download-20261025T151403Z-1-001`.

The proposed scope is model knowledge of Alash scholars' scientific and educational works, their terminology, and relevant publication and intellectual history. General political knowledge is outside the proposed pilot.

## What was reviewed

All 39 OCR JSON files and all 39 terminology workbooks were structurally inspected. All extracted terminology rows were processed, with focused reading of scientific title pages, introductions, terminology passages and selected contents pages. This is a corpus audit and benchmark design review, not a line-by-line scholarly validation of the entire collection. No models were evaluated in this review. No source files were changed.

- 13,195 OCR page records.
- 3,678,351 whitespace-separated words in raw OCR, including front matter and processing artifacts.
- 74,535 candidate terminology row instances: 74,520 in main sheets plus 15 in an additional glossary.
- 7,915 rows have a nonempty `Алаш түсініктемесі` field. A nonempty field is not proof of a verbatim or correct historical definition.
- 50,761 distinct normalized strings in the historical-term field. These are not independently verified concepts or original coinages.
- No byte-identical or whitespace/case-normalized identical full OCR books were detected. Repeated works and passages across editions still need deduplication.
- None of the page image files referenced by the OCR are present in the supplied book directories.

## Confirmed motivating example

The psychology volume of Жүсіпбек Аймауытов has `құлақ қошқары` in `terms.xlsx`, sheet `Sheet`, row 968 (A968:K968). A968 is `ұлу (құлақ ұлуы)`, B968 is `құлақ қошқары`, and F968 contains the supporting passage. The referenced OCR record has `page: 92`, `file: 0092.png`; its printed page footer is **93**. OCR record 93, printed page 94, also uses the term.

The source explicitly says: “Лаберентде құлақ қошқары (улитка) деген бөлім бар.”

This establishes usage and the Russian equivalent in this transcription. It does not establish first coinage, exclusive authorship of the term, or the author's reason for choosing the name. The modern definition in the workbook is a separate annotation and needs scientific review. The title page reproduced in the OCR dates the psychology work to 1926; the workbook's 2013 value belongs to the collected-edition metadata and must not be used as the original work date.

## Findings to resolve before making gold questions

1. **Dates have different meanings and sometimes conflict.** The Ермекұлы workbook reports 1931, while the supplied title pages and printing information show 1935. The Күдерин workbook reports 2013, while its reproduced title page shows 1936. Preserve the values and their provenance, then verify them. Do not automatically treat any single workbook date as the original publication year.
2. **The workbooks use several schemas.** Main sheets have 11, 12 or 14 columns. The Жұмабаев workbook additionally has an empty sheet and a four-column glossary. The Шоқай `Таңдамалы_шығармалар` sheet lacks a header row: 1,650 records were counted using a schema inferred from sampled cells. Import by header name with a documented fallback, rather than by universal column positions.
3. **Raw OCR includes processing messages.** A pattern scan identified 17 records containing English messages such as “I am sorry” or “no visible text”: 2 in Дулатұлы `_2`, 2 in Дулатұлы's educational volume, 11 in Сәтбаев, and 2 in Әуезов. Inspect the original images before deciding whether they represent blank pages or failed transcription. Exclude the messages themselves from scholarly text.
4. **Some OCR coverage is sparse.** Қошке volume 2 has 65 OCR records with IDs spanning 1–326. Шоқай `Таңдамалы_шығармалар_2` has 182 records spanning 1–352. Gaps do not prove that every absent page contained text, but completeness is unverified. Join references using the `page` field, never array index plus one.
5. **Attribution must be attached to individual works.** The Қошке chemistry volume identifies П. Лебедев's textbook and Қошке's translation. The Шонанұлы reading volume contains a textbook coauthored with Байтұрсынұлы. A folder's author is not sufficient evidence that every term was coined by that person.
6. **Scripts and transcription quality vary.** Ермекұлы and Күдерин include historical Latin-script text; other volumes include Arabic-script facsimiles, Cyrillic transcriptions and Russian text. An OCR spelling difference is not automatically a historically distinct term.
7. **Term fields are candidate annotations.** Generic vocabulary, modern publishing terms, historical variants and technical concepts are mixed together. Modern definitions and domain labels are not independently validated labels. Begin with terminology supported by explicit definitions or bilingual equivalents in the actual source.
8. **Historical fidelity and current scientific validity are separate.** A model should faithfully describe a historical scholar's explanation while distinguishing it from a present-day account where necessary. Score these dimensions separately.

## Recommended evaluation

Primary question: **Do models already know the scholarly vocabulary, concepts, works and publication history represented in the corpus?**

The primary track is closed book: no excerpt, retrieval or browsing. Source passages, exact locations and scholarly reviews are available to annotators and graders. A secondary supplied-passage condition measures how much performance changes when evidence is available. Retrieval can follow once the knowledge benchmark is stable.

For a term, create paired directions:

- Term to concept: identify or explain a historical scientific term.
- Concept to historical term: name the term used in a specified author's work, with the target term absent from the prompt.

Also assess faithful explanation of the author's argument and publication history (textbook editions, translations, collaborators, educational work and terminology debates). Ask about use or attestation unless first coinage is independently established.

For `құлақ қошқары`, candidate prompts are:

1. Жүсіпбек Аймауытовтың «Психология» еңбегіндегі «құлақ қошқары» қандай анатомиялық құрылымды білдіреді?
2. Жүсіпбек Аймауытов «Психология» еңбегінде «улитка» деп аталған ішкі құлақ бөлігін қазақша қалай атайды?
3. Аймауытов дыбысты ажыратуды түсіндіруде арфа ішектерінің мысалын қалай қолданады?

These are draft items pending scan verification and independent review. They form one concept/source family and must not be counted as three independent facts. An explanation of why the author chose the word `қошқар` would need additional evidence before becoming a factual gold question.

Other source-backed candidates inspected in the OCR:

| Author/work group | Historical expression | Supporting OCR page ID | Printed footer | Candidate evaluation |
|---|---|---:|---:|---|
| Аймауытов, psychology | құлақ қошқары | 92 | 93 | Meaning, reverse recall, discourse |
| Байтұрсынұлы, Тіл–құрал | қопармалы тіл | 24 | 25 | The author's linguistic classification |
| Досмұхамедов, selected works | хұжайра | 122 | 121 | Biological component and its described properties |
| Омарұлы, geometry | аудандық пішіндеме / көлемдік пішіндеме | 6 | 5 | Distinguish the two geometric branches |
| Омарұлы, physics | бір затты нәрсе / әр затты нәрсе | 6 | 5 | Explain the author's contrast using his examples |
| Жұмабаев, Педагогика | әсерлену | 61 | 61 | Explain the process described in this work |
| Ермекұлы, higher mathematics | title and first-part subject | 1–4 | varies | Edition-specific publication history and work contents |

Suggested pilot: 100 independently reviewed concepts/facts spanning several scientific domains, with terminology as the majority. Paired prompts increase prompt count, not the number of independent facts. Add a small set of separately verified scholarly-history facts. Select the final test size after seeing annotation agreement and paired model disagreement in the pilot.

Grade concept accuracy, historically appropriate wording or accepted variants, requested attribution, fidelity to the scholar's explanation, and unsupported claims. Short-answer evaluation should allow inflection and spelling variants. A model answering only with the modern equivalent can earn concept credit while missing a reverse-recall historical-term requirement. Do not require memorized page numbers; penalize fabricated citations if supplied.

Use two Kazakh-speaking reviewers where possible, including relevant disciplinary expertise for scientific mappings. Blind the model identity during grading. Keep all paraphrases, reverse prompts, translations, repeated terms and overlapping passages from the same concept/work family in the same split. Report intervals clustered by source or concept family and macro-averages by discipline. Include ordinary modern-science control questions to assess whether errors are specific to historical terminology.

For releases, record original work, original author, translator/coauthors, original year, collected edition, edition year, original script, transcription version, OCR page ID, printed page, evidence and annotation provenance. New OCR does not establish absence from model pretraining.

## All-book inventory

The priorities below are scope recommendations from source samples and workbook categories, not claims about political membership or a complete scholarly classification. `Context` means a source may support selected background or publication-history questions; it does not mean it lacks research value.

| ID | Book folder | OCR records | Candidate rows | Proposed use | Main opportunity / note |
|---|---|---:|---:|---|---|
| B01 | Аймауытов_Жүсіпбек__Алты_томдық_шығармалар_жинағы._Психология_жан_жүйесі_мен_өнер_таңдау._Том_4 | 379 | 3,160 | Priority | Psychology, physiology, historical scientific terminology |
| B02 | Асфендиаров_С._Ж.__Шығармалары | 375 | 2,178 | Select excerpts | Education and scholarly history; mixed collected writings |
| B03 | Байтұрсынұлы_Ахмет__Алты_томдық_шығармалар_жинағы._Мақалалар_хаттар_А.Байтұрсынұлы_туралы_құжаттар_мен_материалдар._Т._VI | 371 | 2,655 | Select excerpts | Language and education essays; documents require individual attribution |
| B04 | Байтұрсынұлы_Ахмет__Алты_томдық_шығармалар_жинағы._Оқу_құралы._Т._II | 368 | 2,358 | Priority excerpts | Reading textbook with natural-science material; 23 page IDs absent inside observed range |
| B05 | Байтұрсынұлы_Ахмет__Алты_томдық_шығармалар_жинағы._Т._1 | 356 | 1,225 | Priority excerpts | Literary theory and terminology; 27 page IDs absent inside observed range |
| B06 | Байтұрсынұлы_Ахмет__Алты_томдық_шығармалар_жинағы._Т._V | 361 | 724 | Select excerpts | Educational and reading materials; 22 page IDs absent inside observed range |
| B07 | Байтұрсынұлы_Ахмет__Алты_томдық_шығармалар_жинағы._Том_4 | 380 | 1,842 | Select excerpts | Reading, educational and other collected materials |
| B08 | Байтұрсынұлы_Ахмет__Алты_томдық_шығармалар_жинағы._Тіл_–_құрал_(қазақ_тілі_мен_оқу-ағартуға_қатысты_еңбектері)._Т._III | 342 | 1,169 | Priority | Linguistic terminology and grammatical concepts; 41 page IDs absent inside observed range |
| B09 | Досмұхамедов_Халел__Таңдамалы | 240 | 1,984 | Priority excerpts | Biology, anatomy and scientific essays |
| B10 | Дулатұлы_Міржақып__Алты_томдық_шығармалар_жинағы._1-том | 368 | 1,135 | Select excerpts | Literature and educational context |
| B11 | Дулатұлы_Міржақып__Алты_томдық_шығармалар_жинағы_1 | 390 | 1,687 | Select excerpts | Essays and scholarly or publication history |
| B12 | Дулатұлы_Міржақып__Алты_томдық_шығармалар_жинағы_2 | 399 | 2,381 | Select excerpts | Collected writings; inspect works individually |
| B13 | Дулатұлы_Міржақып__Алты_томдық_шығармалар_жинағы_3 | 504 | 3,263 | Context | Legal and other collected materials; select only relevant scholarly items |
| B14 | Дулатұлы_Міржақып__Алты_томдық_шығармалар_жинағы_4 | 480 | 1,599 | Context | Documents and biographical context |
| B15 | Дәуірдің_жарық_жұлдызы | 245 | 389 | Context | Bibliography and biography of M. Tynyshpaev |
| B16 | Ермекұлы_Ә.__Ұлы_математика_курсы._I—BӨLІM | 161 | 1,715 | Priority after transcription review | Higher mathematics; historical script and formulas |
| B17 | Жұмабаев_Мағжан__Шығармалары._2-том | 372 | 1,105 | Priority | Pedagogy and psychology; includes a supplementary 15-row glossary |
| B18 | Кеменгерұлы_Қошке__Үш_томдық_шығармалар_жинағы._Том_2 | 65 | 410 | Priority excerpts | Language teaching; OCR page coverage is sparse; 261 page IDs absent inside observed range |
| B19 | Кемеңгерұлы_Қошке__Үш_томдық_шығармалар_жинағы | 378 | 1,871 | Select excerpts | Agricultural, educational and other collected writings |
| B20 | Кемеңгерұлы_Қошке__Үш_томдық_шығармалар_жинағы._Том_3 | 383 | 4,266 | Priority | Chemistry translation and dictionary; distinguish translator and co-compilers |
| B21 | Күдерин_Жұмақан__Қант_қызылшасы | 48 | 672 | Priority after transcription review | Agronomy; historical Latin script; 21 page IDs absent inside observed range |
| B22 | МІРЖАҚЫП_ДУЛАТҰЛЫ__АЛТЫ_ТОМДЫҚ_ШЫҒАРМАЛАР_ЖИНАҒЫ._4-том._Ағартушылық_бағыттағы_еңбектері_мен_оқу_құралдары | 342 | 1,278 | Priority | Educational works, arithmetic and reading textbooks |
| B23 | НӘЗІР_ТӨРЕҚҰЛОВ__КӨП_ТОМДЫҚ_ШЫҒАРМАЛАР_ЖИНАҒЫ._2._Доклады_выступления_письма | 255 | 1,229 | Context | Collected reports and documents; select scholarly passages |
| B24 | НӘЗІР_ТӨРЕҚҰЛОВ__КӨП_ТОМДЫҚ_ШЫҒАРМАЛАР_ЖИНАҒЫ._3-том_Баяндамалар_естеліктер_зерттеулер | 286 | 1,972 | Select excerpts | Language and education within collected writings |
| B25 | НӘЗІР_ТӨРЕҚҰЛОВ__Шығармаларының_көп_томдық_жинағы._1-том._Зерттеулер_мақалалар | 263 | 1,612 | Select excerpts | Language, publishing and scholarly discourse |
| B26 | Омарұлы_Елдес__Үш_томдық_шығармалар_жинағы._II_том._Физика | 409 | 3,745 | Priority | Physics and historical scientific terminology |
| B27 | Омарұлы_Елдес__Үш_томдық_шығармалар_жинағы._I_Том | 374 | 2,869 | Select excerpts | Linguistic and other collected scholarly writings; 27 page IDs absent inside observed range |
| B28 | Омарұлы_Елдес__Үш_томдық_шығармалар_жинағы._ІІІ_Том | 421 | 1,519 | Priority | Geometry; distinguish original works, translations and editions |
| B29 | Санжар_Асфендияров__Санжар_Асфендияров | 378 | 2,764 | Context | Biography, scholarly history and collected materials |
| B30 | Сәтбаев_Қ.__Тандамалы | 384 | 3,692 | Adjacent scientific heritage | Geology and scientific institutions; define its relation to the core author list |
| B31 | Шонанұлы_Телжан__Бес_томдық_шығармалар_жинағы_1 | 242 | 1,914 | Priority excerpts | Reading textbook and science; coauthored works require attribution |
| B32 | Шонанұлы_Телжан__Бес_томдық_шығармалар_жинағы_2 | 256 | 1,502 | Priority excerpts | Literacy and teaching methodology; coauthored works require attribution |
| B33 | Шонанұлы_Телжан__Үш_томдық_шығармалар_жинағы._1-том | 383 | 1,878 | Select excerpts | Education and agricultural or economic material |
| B34 | Шонанұлы_Телжан__Үш_томдық_шығармалар_жинағы._Т._3 | 375 | 2,257 | Select excerpts | Language, teaching and other collected writings |
| B35 | Шоқай_Мұстафа__Тандамалы_шығармалар | 392 | 1,515 | Context | Use verified scholarly or publication-history excerpts |
| B36 | Шоқай_Мұстафа__Таңдамалы | 513 | 2,182 | Context | Use verified scholarly or publication-history excerpts |
| B37 | Шоқай_Мұстафа__Таңдамалы_шығармалар | 383 | 1,650 | Context | Headerless terminology sheet; use verified scholarly excerpts |
| B38 | Шоқай_Мұстафа__Таңдамалы_шығармалар_2 | 182 | 990 | Context | Sparse OCR coverage; use verified scholarly excerpts; 170 page IDs absent inside observed range |
| B39 | Әуезов_М._О.__Шығармаларының_елу_томдық_толық_жинағы | 392 | 2,179 | Priority excerpts | Literary scholarship and educational or scientific reading materials; 66 page IDs absent inside observed range |

## Suggested first action

Choose the psychology, linguistic, biology, physics and geometry sources. Verify 20 term/concept pairs against scans and original-work attribution. Write both question directions without consulting model answers, have another reviewer answer them, then run the existing Qwen pair. This establishes whether the dataset and scoring can distinguish historical-term knowledge from general scientific understanding before expanding to the full collection.
