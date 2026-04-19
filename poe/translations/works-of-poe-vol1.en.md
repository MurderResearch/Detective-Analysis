# The Works of Edgar Allan Poe — Volume 1 — Deducibility Analysis

## Metadata
- Author: Edgar Allan Poe
- Year: 1903 (Raven Edition); the works collected were originally published 1842–1843
- Type: Short story collection (this analysis focuses on the two detective works within)
- Detective: Chevalier C. Auguste Dupin (The Mystery of Marie Rogêt); William Legrand (the amateur cryptographer of The Gold-Bug)
- Core mystery type: Cryptographic puzzle (The Gold-Bug) + armchair detection / media analysis (The Mystery of Marie Rogêt)

---

## Overall Difficulty Rating

This volume collects multiple works. The present analysis takes up the two that possess an explicit detective-reasoning structure — **The Gold-Bug** and **The Mystery of Marie Rogêt** — treating each in turn, before offering an overall evaluation for the volume's detective pieces. The Murders in the Rue Morgue is likewise included in this volume, but it has already been analyzed separately as D1 and will not be repeated here.

| Metric | Stars | Notes |
|--------|-------|-------|
| Deducibility | ⭐⭐⭐⭐ | Average convergence point about 78% — both works defer the key decoding clues to the final sections before revealing them in full |
| Fog Rating | ⭐⭐⭐ | The Gold-Bug uses Legrand's feigned madness to mislead the reader; Marie Rogêt constructs moderate fog through a mass of contradictory newspaper reports |

---

## Synopsis

### The Gold-Bug (1843)
The bankrupt aristocrat Legrand lives in seclusion on Sullivan's Island in South Carolina, in the company of his elderly Black servant Jupiter and a Newfoundland dog. One day he picks up a golden beetle and an old piece of parchment on the shore. Several weeks later his behavior turns strange; he insists that the narrator "I" and Jupiter accompany him into the mountains of the mainland to search for treasure. The party climbs a great tulip tree, finds a skull nailed to one of its branches, lowers the gold-bug through an eye socket of the skull to fix the position, and, digging there, unearths a chest full of gold and jewels — the lost treasure of the seventeenth-century pirate Captain Kidd. Afterwards Legrand explains to the narrator that the parchment bore a ciphered text written in invisible ink that appears only when heated; by means of frequency analysis he deciphered it, drawing out such clues as "Bishop's Hostel," "Devil's Seat," "the seventh limb east side of the main trunk," and "the left eye of the skull," and so progressively pinned down the location of the treasure.

### The Mystery of Marie Rogêt (1842–1843)
The sequel to Rue Morgue. Marie Rogêt, a Parisian perfumery shopgirl (a figure alluding to the real case of the 1841 New York cigar-shop girl Mary Rogers), goes missing; three days later her body surfaces in the Seine — marks of strangulation on the neck, clothes torn, beaten and then dumped. The police are at a loss and turn to Dupin. Dupin never leaves his apartment throughout the case; relying on newspaper clippings alone as evidence, **he reasons by media-text analysis** and concludes: the body is indeed Marie's; the crime is the work of a single man and not a gang; the murderer is a swarthy naval officer (likely the "naval petty officer" with whom she went off during her first disappearance); the scene of the crime is a thicket near Mme Deluc's inn; the body was transported by boat. In a closing footnote Poe explains that he has offered a fictional reading of a real unsolved case; later confessions by two of the parties involved substantially confirmed Dupin's deductions.

---

## Truth Breakdown

### Part One: The Gold-Bug

#### Truth #1: The meaning of the parchment cipher (howdunit)

- **Clue convergence point: about 82%**
- Answer: The cipher uses a simple letter-substitution scheme; deciphered, it reads "A good glass in the bishop's hostel in the devil's seat forty-one degrees and thirteen minutes northeast and by north main branch seventh limb east side shoot from the left eye of the death's-head a bee line from the tree through the shot fifty feet out" — that is, starting from the old Bessop family seat, sighting through the hollow in the "Devil's Seat" with a telescope to locate the skull in the tree, drop a line fifty feet through the skull's left eye, and there lies the spot where the treasure is buried.

##### Key Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | The "beetle" Legrand draws is in fact a death's-head pattern (the reverse of the parchment shows it when warmed) | ~15% | The first anomalous signal in the story — the skull being a pirate's classic insignia |
| 2 | The object picked up is parchment, not ordinary paper — implying it was meant to be kept for a long time | ~42% | Suggests the object carries an important record |
| 3 | A cipher written in heat-sensitive invisible ink appears on the parchment | ~48% | The puzzle formally enters the story |
| 4 | Legrand breaks the cipher through letter-frequency analysis (8 appears most often → e) | ~55–70% | A concrete demonstration of the reasoning method; the most important didactic passage in the story |
| 5 | The pun on "Captain Kidd" — the figure of a "kid" (a young goat) on the parchment serves as a signature | ~60% | Fixes the language of the cipher as English and the author's identity as Kidd |
| 6 | "Bishop's Hostel" corresponds to the rock formation of the Bessop family; "Devil's Seat" is a natural hollow in the rock | ~78% | The final step translating the text cipher into a real-world coordinate |
| 7 | Jupiter lowers the gold-bug through the "right" eye of the skull (he cannot tell left from right), causing a 2.5-inch displacement → magnified into a large offset at fifty feet | ~82% | The ultimate verification point in the reasoning — the treasure is found after correction |

##### Supporting Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | Near the spot where the item was picked up lies the wreckage of an old ship | ~44% | Echoes the pirate theme |
| 2 | Legends of Kidd's treasure have circulated for ages but it has never been found | ~52% | Reinforces the inference that the buried item is real |
| 3 | At a specified height on the tulip tree (the seventh limb) a skull has been nailed | ~75% | Confirms that the cipher's instructions point to a physically verifiable object |
| 4 | The iron ring (one of the handles of the iron chest) unearthed causes the narrator to stumble | ~80% | Verifies that the location is correct |

##### Red Herrings

| # | Clue | Position (%) | Misleading direction |
|---|------|--------------|----------------------|
| 1 | Legrand's sudden strange behavior, pallor, and Jupiter's suspicion that he "has gone mad from the gold-bug's bite" | ~15–30% | Leads the reader (together with the narrator "I") to misjudge the protagonist as mentally unhinged |
| 2 | Jupiter's insistence on the weight and metallic luster of the beetle | ~5–20% | Misleads the reader into thinking that "the gold-bug is real gold" — a surface mystery — is what matters |
| 3 | Legrand's theatrical gesticulations with the beetle beneath the tree, like a sorcerer | ~72% | Legrand afterwards admits this was deliberate performance — a piece of "cool mockery" — for the narrator's benefit: an entire stretch of behavior as performance art, a red herring |

---

#### Truth #2: Why Legrand feigned madness (whydunit)

- **Clue convergence point: about 95%**
- Answer: Legrand's head has been perfectly clear from start to finish. That he lets the narrator think him mad, and insists on having Jupiter drop the beetle through the skull's eye (instead of the more rational choice of a bullet), is because he perceives the narrator's own doubts about his mental state and resolves, as a quiet retaliation, to indulge in "a little bit of mystification."

##### Key Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | Before the treasure is dug up, Legrand has already gone into the mountains alone and personally surveyed both the "Bishop's Hostel rock" and the tulip tree | ~88% | Proof that all his actions were pre-planned, not the random conduct of a madman |
| 2 | Legrand afterwards volunteers the confession: "In return for your suspicions I resolved to punish you with a little quiet mystification" | ~95% | The final confession — the emotional reversal of the story |

##### Supporting Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | Legrand's precise measuring, staking, and clearing of the circular area are carried out in orderly fashion | ~70–78% | These operations are inconsistent with the image of a madman |
| 2 | Legrand shows a peculiar sensitivity to any tone in the narrator that "doubts my sanity" | ~30% | Plants the seed for the final revelation |

---

### Part Two: The Mystery of Marie Rogêt

#### Truth #1: Confirming the identity of the deceased (whoisit — is the body Marie herself?)

- **Clue convergence point: about 25%**
- Answer: The floating body is indeed Marie Rogêt. Dupin refutes the L'Etoile newspaper's contention that "the body had been in the water too short a time, and therefore cannot be Marie," pointing out the logical flaws of that argument by means of probability theory and the principle of bodily density.

##### Key Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | On the body is found a garter whose buckle has been "set back" to shorten its length — a known habit of Marie's | ~22% | A single item is not itself decisive, but as multiple pieces of physical evidence accumulate the probability rises geometrically |
| 2 | Gloves, the flowers on the small hat, shoes, height, build and many other items match Marie exactly | ~22% | Dupin's argument: any one of these taken alone might not be decisive, but their simultaneous agreement approaches certainty |
| 3 | Dupin demonstrates that a body's floating time is not necessarily "6–10 days"; following a violent death without drowning, the body may never sink at all | ~24% | The sole scientific basis for refuting L'Etoile's claim |

##### Red Herrings

| # | Clue | Position (%) | Misleading direction |
|---|------|--------------|----------------------|
| 1 | L'Etoile's report that "Marie may still be alive and the body belongs to another" | ~18% | Misleads the public through sensational speech; Dupin criticizes the argument as resting on unverified assumptions |
| 2 | The suspicion cast on Beauvais (the rose at the keyhole, the slate by the door with "Marie" written on it) | ~19% | Makes the reader think Beauvais may be involved; Dupin points out that these are merely the products of "amorous fussiness" |

---

#### Truth #2: The pattern of the crime (gang or individual?)

- **Clue convergence point: about 65%**
- Answer: The work of a single individual, not a gang. Dupin reasons, from the fact that a 30,000-franc reward has drawn no informer, that had it been a gang one of its members would certainly have betrayed the others for the sake of the reward or of a pardon — only when the facts are known to one man alone can the secret be kept so tightly.

##### Key Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | The bonnet-string is fastened by a "sailor's knot" (not a lady's knot) | ~30% | Points to the murderer being a sailor / navy man |
| 2 | A strip torn from the dress was wrapped around the waist as a "carrying handle" for the body — rational if the murderer had to move the corpse alone after the act in the thicket, unnecessary if a gang were carrying it | ~58% | The design's intent reveals a murderer moving the body alone |
| 3 | Abrasions and pressure marks on the back and shoulder-blades of the body correspond to the rib of a boat, implying the body was thrown from a boat | ~62% | Points to the use of a boat by the murderer |
| 4 | A reward of 30,000 francs is offered, with a promise of pardon to accomplices, yet after several weeks no one informs | ~65% | Dupin's most devastating probabilistic argument: silence itself is evidence of a lone crime |

##### Supporting Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | Mme Deluc witnesses, on the day in question, a man and a woman arriving first at the inn; the man of dark complexion | ~32% | Consistent with the characteristics of a sailor |
| 2 | At dusk a party of coarse men leaves the inn (the press misidentifies them as the murderers), but their movements do not match the later sequence in which screams are heard after nightfall | ~60% | Dupin points out that the press has overlooked the time difference |
| 3 | The omnibus driver Valence personally sees Marie crossing the river in the same boat with a man of dark complexion | ~35% | A direct witness, pinning down the type of the murderer |

##### Red Herrings

| # | Clue | Position (%) | Misleading direction |
|---|------|--------------|----------------------|
| 1 | The widely reported "gang-attack theory" in the press | ~40% | The narrative generally accepted by public opinion at the time; Dupin refutes it point by point through logic |
| 2 | Marie's fiancé St. Eustache poisons himself, seemingly out of guilt | ~38% | In fact the result of grief at losing his beloved; he leaves a suicide note |
| 3 | Clothing found in the thicket said to bear "mildew marks of several weeks' standing" | ~45% | Le Soleil claims the clothes had lain in the thicket for weeks — Dupin questions whether, if so, two boys would not have found them earlier, and observes that the mildew could easily be the result of three or four damp days |

---

#### Truth #3: The identity of the murderer (whodunit)

- **Clue convergence point: about 95%** (limited by Poe's deliberate refusal to name him)
- Answer: Pointing toward the "naval officer" who accompanied Marie during her earlier, brief disappearance — dark of complexion, of naval experience, and familiar with the mooring of barges (able to recover a rudderless boat without advertising for it in the press). Poe deliberately closes the story with the editorial footnote "for manifest reasons we omit the steps of the pursuit," while making it plain that Dupin has succeeded in solving the case.

##### Key Clues

| # | Clue | Position (%) | Notes |
|---|------|--------------|-------|
| 1 | Marie's first disappearance (from which she returned alone a week later) was rumored to have been an elopement with a "naval officer" | ~12% | Plants the single most important foreshadowing — the murderer may be an old acquaintance |
| 2 | The murderer used a boat to dispose of the body → the boat was recovered at dawn the next day by the barge-master → later that same day someone retrieved the boat (but not the rudder) → this person knew the boat's whereabouts without any newspaper announcement | ~88% | Such a chain of reasoning can point only to a navy man with daily links to maritime business |
| 3 | Dark complexion + sailor's knot + a social standing higher than an ordinary sailor's (able to be seen in the company of a girl like Marie, not of the lowest class) | ~65–88% | The intersection of these three clues shrinks the pool of suspects to a very small number |

---

## Reasoning Path Reconstruction

### The Gold-Bug

The first strand of reasoning (the cipher itself) is Poe's **lesson in cryptography** for the reader — by way of frequency analysis, common doubled letters (ee), and common three-letter groupings (the), the reader can work out each letter in turn. Any reader of English can, in principle, follow Legrand's steps and crack it himself. The clues converge at about 82% — when the deciphered coordinates have all been translated into a real-world position and then, after the "left-eye / right-eye" correction, are fully verified.

The second strand (whether Legrand is mad) is a classically Poe-esque psychological experiment: the author knows the reader will take the narrator "I"'s point of view and doubt the protagonist's sanity, and yet he quietly supplies counter-evidence through Legrand's precise measurements. The true convergence point is in the final confession (95%) — but a sharp reader should already begin to doubt, around the 70% mark of the measuring scenes, why a "madman" could be so systematic.

### The Mystery of Marie Rogêt

This is the earliest instance in detective literature of **pure media-analysis reasoning** — Dupin never leaves the apartment, never interviews a single witness, never examines the body; he works solely from newspaper clippings and restores the truth by logical elimination. The reader's path of reasoning must follow Dupin's three layers in order:
1. Confirming the identity of the body (convergence about 25%) — criticizing L'Etoile's misuse of probability
2. Ruling out a gang crime (convergence about 65%) — through the triple cross-check of the unclaimed reward's probability argument, the sailor's knot, and the corpse-carrying design
3. Pinning down the type of the murderer (convergence about 88%) — by taking the anomaly of the rudder's secret retrieval and reasoning backwards to the murderer's daily link to maritime business

**Threshold of reading**: this tale is harder than The Gold-Bug, because all key clues are hidden in fictional news copy; the reader must, like Dupin, resist the sensational narrative of the press and carry out the probability assessments personally.

---

## Remarks

### The Gold-Bug's place in the history of detective fiction

The Gold-Bug is **the earliest work in detective fiction to make cryptography its core**. In this tale Poe lays out, almost in the manner of a scholarly paper, the methodology for breaking a classic letter-substitution cipher (frequency analysis, common combinations, punning glyphs). The work inspired a vast lineage of later cryptographic detective stories, from Doyle's "The Adventure of the Dancing Men" (1903) to the entire career of Dan Brown.

What is intriguing is that Legrand is not a "detective" but a "decipherer-cum-treasure-hunter" — he is not solving a case but solving a puzzle. This makes The Gold-Bug a prototype of **"pure intellectual reasoning"**: no murderer, no victim (Kidd and his helpers in the burial died a century ago) — only an encrypted sheet of paper and a set of coordinates to be resolved.

### The experimental genre-crossing of The Mystery of Marie Rogêt

This may be the boldest hybrid-genre experiment in literary history: Poe took a real unsolved murder case (the 1841 murder of Mary Rogers in New York), moved it to Paris, changed the names and the river's name, and let his fictional detective Dupin "solve" the case from newspaper clippings. This is not only fiction, it is **investigative commentary published in fictional form**.

Poe's ambition does not stop there — in his closing footnote he states outright that he has offered a reading of the real case. Later the deathbed confession of Madame Deluc (the same figure in the real case) and the confession of another involved party substantially confirmed Dupin's deductions (a single-handed crime, the scene in a thicket near the inn, the murderer an acquaintance of Marie's). This makes The Mystery of Marie Rogêt the first instance of **"a detective story influencing an actual investigation"** — half a century earlier than the comparable cases connected with Sherlock Holmes.

### The differing philosophies of detection in the three Dupin stories

| | The Murders in the Rue Morgue | The Mystery of Marie Rogêt | The Purloined Letter |
|--|-------------------------------|----------------------------|-----------------------|
| Core problem | Physical impossibility | Informational ambiguity | Psychological blind spot |
| Type of culprit | Non-human (an orangutan) | A man (a naval officer) | A man (Minister D——) |
| Source of evidence | Physical evidence at the scene | Newspaper text | Psychological reasoning |
| Method of reasoning | Observation + imagination | Probability theory + logic | Reading character + game theory |

The Murders in the Rue Morgue demonstrates "observation"; The Mystery of Marie Rogêt demonstrates "analyzing texts"; The Purloined Letter demonstrates "reading people" — Poe's trilogy completely covers the three great epistemic bases of classical detective fiction.

### A brief note on the other, non-detective pieces in the volume

This volume also contains "The Unparalleled Adventure of One Hans Pfaall" (science fiction), "Four Beasts in One" (political satire), "The Balloon-Hoax" (scientific satire), "MS. Found in a Bottle" (Gothic nautical), and "The Oval Portrait" (Gothic parable of art) — each a representative piece of Poe in its own genre, but none possessing a structure of detective reasoning, and so not included in the present analysis.

### A note for Taiwanese readers

In The Gold-Bug, Poe's depiction of the Black servant Jupiter makes heavy use of 19th-century African-American Southern dialect and carries stereotypes that modern readers find difficult to accept (for example, treating Jupiter's inability to distinguish left from right as "stupidity"). This reflects the social reality of the American South in 1843 and has made The Gold-Bug a standard case in contemporary literary education for discussing "race in detective fiction." In reading one may take Jupiter's dialect as a historical record; but Jupiter's loyalty, thoughtfulness, and delicacy of feeling are in fact what make him the most three-dimensional character in the story — Poe does not reduce him to a mere clown.
