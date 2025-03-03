# CHANGELOG


## v0.13.4 (2025-02-23)


## v0.13.3 (2025-02-23)

### Bug Fixes

- We expose the attachment model so that it can be used in the API
  ([`5e0b602`](https://github.com/nguaman/licitpy/commit/5e0b60243b64350b2c9bdeac36369960af310e5f))

- We expose the Item, Question, Renewal, and Subcontracting models
  ([`f0ab927`](https://github.com/nguaman/licitpy/commit/f0ab927b829696818506cf13f95873728d601a5f))


## v0.13.2 (2025-02-21)

### Bug Fixes

- We optimized the logic for obtaining bids from the API and the CSV
  ([`85334f7`](https://github.com/nguaman/licitpy/commit/85334f71ae8ebc81097a2c324b43723306fed3bf))


## v0.13.1 (2025-02-21)


## v0.13.0 (2025-02-18)

### Bug Fixes

- Omit bidding code when it is not yet available in the OCDS API of Mercado Público
  ([`773359c`](https://github.com/nguaman/licitpy/commit/773359c1f698348692405f5cb03ac3434611c5d9))

### Features

- Added the table information with the details of the proposals in the award
  ([`09222a7`](https://github.com/nguaman/licitpy/commit/09222a7b3795451aeb7bae1f1e0be906b4251dc9))


## v0.12.0 (2025-02-12)


## v0.11.0 (2025-02-11)

### Bug Fixes

- We updated the packages and followed Bandit recommendations
  ([`62cfa56`](https://github.com/nguaman/licitpy/commit/62cfa568dcc661bbe7f3aae8c39293d427bbd58f))

### Features

- We added the ability to download attachments from the awarded tender view using the same code to
  download the tender attachments
  ([`61bdb0d`](https://github.com/nguaman/licitpy/commit/61bdb0d9893b926bd4ecb23460ac241d56fb0aec))


## v0.10.0 (2025-01-11)

### Features

- Added whether subcontracting is allowed and whether it is a renewable tender
  ([`f1873ad`](https://github.com/nguaman/licitpy/commit/f1873ad407559ca64ed952cf9716c260ffff9efd))

- We added the Awarded entity and added support for Python 3.12
  ([`a3f8e27`](https://github.com/nguaman/licitpy/commit/a3f8e274b99727da4df073aa5a7b2ea626a98243))


## v0.9.0 (2025-01-11)

### Features

- We detect when the tender has standardized bases
  ([`a93e898`](https://github.com/nguaman/licitpy/commit/a93e89822c0b6918560bdec7500e751d7cd1cf60))


## v0.8.4 (2024-12-15)

### Bug Fixes

- Additional tests, integration with isort and black, and testing triggers on the publish GitHub
  Action
  ([`349398f`](https://github.com/nguaman/licitpy/commit/349398f769996ab0e6e4977f0b7e2d39bee3ef56))

### Continuous Integration

- Add skip-existing: true to avoid conflicts if the version already exists
  ([`7c5e5a2`](https://github.com/nguaman/licitpy/commit/7c5e5a29660c20c031a98763112169bf7b8dade3))

### Testing

- Add more tests
  ([`c45384a`](https://github.com/nguaman/licitpy/commit/c45384a7ba3da95c3115e4d40b0a7ee19825f680))


## v0.8.3 (2024-12-14)

### Bug Fixes

- Minor fixex - github action
  ([`b2f3f51`](https://github.com/nguaman/licitpy/commit/b2f3f51afb92775fb200f782ea4da68d6dd3c730))

### Documentation

- Adding basic comments
  ([`79d7b20`](https://github.com/nguaman/licitpy/commit/79d7b20530e69c01ea955acd72e48f3130b0414d))


## v0.8.2 (2024-12-14)

### Bug Fixes

- Minor fixes and first notebook
  ([`c0a0d38`](https://github.com/nguaman/licitpy/commit/c0a0d3825af73d96432b94f4ebdd36958ef9b7ce))

### Continuous Integration

- Add branch filter for 'main' in publish workflow
  ([`8a68561`](https://github.com/nguaman/licitpy/commit/8a68561e680856c117b4629acdd7dc30af22788a))


## v0.8.1 (2024-12-14)

### Bug Fixes

- Fix of the tag in GitHub Actions publish.yml to trigger correctly
  ([`2d5a1b2`](https://github.com/nguaman/licitpy/commit/2d5a1b253dd064b2ef646d7b4b41df4e55bbc5af))


## v0.8.0 (2024-12-14)

### Features

- All tenders will have a closing date. Improved logic for obtaining tenders based on the OCDS API
  and CSV. Created the first integration tests
  ([`40ec62f`](https://github.com/nguaman/licitpy/commit/40ec62f8945171882dabcf2f2709fa6ed92789e5))


## v0.7.0 (2024-12-11)

### Continuous Integration

- Add workflow_dispatch
  ([`d6b9ff2`](https://github.com/nguaman/licitpy/commit/d6b9ff202fe15d288f089d44d2ac88e665f6bc17))

### Features

- We added the parsing of items for tenders
  ([`e3e3140`](https://github.com/nguaman/licitpy/commit/e3e3140a9e685cdf238cb3575dea8a2f225cf43c))


## v0.6.1 (2024-12-10)

### Bug Fixes

- Correction of the tenders parser and addition of more file extension types
  ([`78c70c2`](https://github.com/nguaman/licitpy/commit/78c70c2abb7a713b0634841f16f25bfe503222fe))

### Continuous Integration

- Add Trusted Publisher Management (Pypi)
  ([`74530e2`](https://github.com/nguaman/licitpy/commit/74530e227b40f44db48b84cd81e288a1cead5b10))

- Remove topics
  ([`b6461f4`](https://github.com/nguaman/licitpy/commit/b6461f49e70d2a1719da8a7be08f8fb7f2f7168a))


## v0.6.0 (2024-12-10)

### Continuous Integration

- Add environment
  ([`cb76f51`](https://github.com/nguaman/licitpy/commit/cb76f51ca3c96adbd137fb34aba24b284326931b))

- Avoid using bash
  ([`7ff564e`](https://github.com/nguaman/licitpy/commit/7ff564e7da4c2ec0b77db1a24ad988c4d607eec4))

- Github Action is triggered when changes are made to the main branch
  ([`05dcc59`](https://github.com/nguaman/licitpy/commit/05dcc5968d81e72ad2cbaf93c96c4af2b59eebfa))

### Features

- Tender questions
  ([`9c6d62d`](https://github.com/nguaman/licitpy/commit/9c6d62dd31a5e6d35bba2370dfa596f7ce7c8b91))


## v0.5.0 (2024-12-08)


## v0.5.0-alpha.1 (2024-12-08)

### Features

- - We added tox, bandit, and retrieving the OC region
  ([`6ef75f8`](https://github.com/nguaman/licitpy/commit/6ef75f85337f13f57a6f43ac265cba8c342402a8))


## v0.4.1 (2024-12-05)

### Bug Fixes

- Purchase orders have their own client, allowing you to search for purchase orders directly
  ([`485294a`](https://github.com/nguaman/licitpy/commit/485294ae1753f733ab02cd62692e159cc63ec677))


## v0.4.0 (2024-11-30)


## v0.4.0-alpha.1 (2024-11-30)

### Features

- Add Purchase Order entity
  ([`aaa042d`](https://github.com/nguaman/licitpy/commit/aaa042d8bf9a55a4e8c459413fa066d31026d488))


## v0.3.0 (2024-11-29)


## v0.3.0-alpha.1 (2024-11-29)

### Documentation

- Add examples
  ([`6a41ab5`](https://github.com/nguaman/licitpy/commit/6a41ab5ff3bb52cb1189fdbc4d5e327b68447ddf))

### Features

- Download of metadata, URL, and the content in base64 of the attached files
  ([`754eeca`](https://github.com/nguaman/licitpy/commit/754eecae6e72745efc6dd92028c78f06a8fa55c1))


## v0.2.5 (2024-11-29)

### Bug Fixes

- Name "date" is not defined
  ([`56c3612`](https://github.com/nguaman/licitpy/commit/56c3612a5cbc5e860113b3803292d5c3bcbb6a5a))

### Documentation

- Change version
  ([`b352966`](https://github.com/nguaman/licitpy/commit/b352966ad7fbbe19a4a70a65cb0a39ef69656911))


## v0.2.4 (2024-11-29)

### Bug Fixes

- Update semantic-release configuration for versioning
  ([`d35e2c0`](https://github.com/nguaman/licitpy/commit/d35e2c062129b47349229d79dd5d9ccb9d04c21f))

### Build System

- Change version
  ([`cbcff1a`](https://github.com/nguaman/licitpy/commit/cbcff1a493b06a94ef6d1e951624fb118fa33aae))


## v0.2.3 (2024-11-29)

### Bug Fixes

- Title, Description, and Opening Date not included in the creation of the Tender entity
  ([`62eb9ae`](https://github.com/nguaman/licitpy/commit/62eb9aecb4804ddcf8c26db535a3f826464c163b))


## v0.2.2 (2024-11-29)

### Bug Fixes

- Fix format of tender codes
  ([`c12d0e0`](https://github.com/nguaman/licitpy/commit/c12d0e03b1b88a3d502773901e57133461310435))


## v0.2.1 (2024-11-29)

### Bug Fixes

- Fix format tender code : 1375735-1-L124
  ([`182337f`](https://github.com/nguaman/licitpy/commit/182337f8e24b9ca532322500d497f6cc14977beb))


## v0.2.0 (2024-11-28)


## v0.2.0-alpha.1 (2024-11-28)

### Documentation

- Add docstrings to entities
  ([`2135d8f`](https://github.com/nguaman/licitpy/commit/2135d8f8edcd4ca3c5339456e256d32aa2d194c6))

### Features

- Improve codebase with mypy and pytest integration, fix download issues, and enhance various
  sections of the code
  ([`b1d16d2`](https://github.com/nguaman/licitpy/commit/b1d16d28d673bc61dd9d787ae1c340273f474f25))


## v0.1.0 (2024-11-16)

### Build System

- Add initial project configuration
  ([`16cf6f9`](https://github.com/nguaman/licitpy/commit/16cf6f9f3ce65c583fc67e0d772a69c8aa58697f))

- Added .gitignore to configure ignored files - Added LICENSE file to define the project license -
  Added README.md with initial documentation

### Continuous Integration

- Consolidate workflows by updating release.yml
  ([`13a1c65`](https://github.com/nguaman/licitpy/commit/13a1c65a2976f8000a333ccc7689da79c9aef07f))

- Consolidate workflows by updating release.yml and removing test.yml
  ([`02bb388`](https://github.com/nguaman/licitpy/commit/02bb388d4c24f25a49e9b04feec1631d7f0f1349))

- Simplify workflows to use Python 3.11 only
  ([`03ff9d4`](https://github.com/nguaman/licitpy/commit/03ff9d4953d88149ed584aaba13aea8bd4516943))

### Features

- Initial features for version 0.1.0
  ([`b443454`](https://github.com/nguaman/licitpy/commit/b443454c1aebe876af7775dee3c295f46d9f1a4b))
