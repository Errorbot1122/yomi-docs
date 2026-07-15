.. _ydoc-contributing-docs:

Writing General (Article) Documentation
=======================================

.. include:: /_snippets/ai-warning.rst

.. include:: /_snippets/new-contrib.rst

.. _ydoc-contributing-docs-goals:

Documentation Goals
-------------------

When writing :ref:`articles <yverb-article>`, your goals should align with the following.

 * Make it **accessible** to new *Modders*.
 * Make it **accessible** to new *Contributors*.

If you follow those 2 rules, you should write great documentation!

.. rst-class:: make-accordion

What is RST?
------------

Similar to the :ref:`Godot Docs <doc_contributing_to_the_documentation>` we use the **Sphinx** ``.rst`` *(* `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ *)* file format, witch is essentially just a more capable `Markdown <https://www.markdownguide.org/basic-syntax/>`_ file.

If you are used to markdown, here is a mini cheat sheet for a few of the important changes:

.. code-block:: rst

   Markdown -> reStructuredText
   ============================

   _Italics_ -> *Italics*
   **Bold** -> **Bold**
   `code` -> ``code``
   [display text](link.org) -> `display text <link.org>`_
   # Header 1 -> Header 1
                 ========
   ## Header 2 -> Header 2
                  --------
   ### Header 3 -> Header 3
                   ^^^^^^^^
   ```txt        .. code-block:: txt
   code block ->    
   ```              code block
   - list item -> * list item
   <small>Raw HTML</small> -> :raw-html:`<small>Raw HTML</small>`
                              OR
                              .. raw:: html
                                 
                                 <small>Raw HTML</small>

*Here are some extra things you should know:*

 * You cannot nest multiple formating directives in one line!
   *(This means no:* ``bold+italics``, ``link+inline-code``, *or* ``bold+ref``. *you must separate them)*
 * Just like *Markdown* you can have a single paragraph span
   multiple
   lines.
 * To write a comments, enter ``.. [COMMENT TEXT]``.
 * You can create custom jump point by writing ``.. _[JUMP_NAME]:`` before any peice of text, then use ``:ref:`Display Text <[JUMP_NAME]>``` to automatically create a link to it.
 * The characters below the *Header* **must be** the same length as the header text itself.
 * The ``.. toctree::`` directive is used to build the sidebar, however can get confusing somtimes.
   Read the `.. toctree:: Documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree>`_ if you ever get stuck.

*(This is just a snippet of all RST can do, check out the* `Sphinx RST Docs <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ *for more of a deep dive on all the things you can do with it.)*

.. _ydoc-contributing-docs-guidelines:

Guidelines
----------

Guidelines to use when writing :ref:`articles <yverb-article>`.

These are some of the rules we like to follow when contributing to this project's :ref:`article <yverb-article>` files. If you want to edit a :ref:`Class Reference <ydoc-class-reference>` file, read :ref:`ydoc-contributing-classes` instead.

To start off, we recommend you reading both the Godot :ref:`doc_content_guidelines` and :ref:`doc_docs_writing_guidelines` as those are the biases for our guidelines.

.. include:: /_snippets/guideline-note.rst

Humor
^^^^^

As you can probably tell, these docs are full of little tidbits of humor.
That's okay, since writing can get boring somtimes, and weaving in small jokes, make everyone happy!

However, this doesn't mean you should **OVER DO IT**!

Remember our man goal is to keep to docs accessible, and to meny jokes can confuse readers into what is important.
So if you have a joke, your best bet is to insert it into a comment inside the raw ``rst`` and we will keep the funniest ones.

Paragraphs
^^^^^^^^^^

When writing paragraphs in an :ref:`article <yverb-article>`, each sentence should be separated by a **new line**.

**DONT:**

.. code-block:: rst

   Godot is meant to be used with its editor. We recommend you give it a try, as it will most likely save you time in the long term. There are no plans to make Godot usable as a library, as it would make the rest of the engine more convoluted and difficult to use for casual users.

   If you want to use a rendering library, look into using an established rendering engine instead. Keep in mind rendering engines usually have smaller communities compared to Godot. This will make it more difficult to find answers to your questions.

**DO:**

.. code-block:: rst

   Godot is meant to be used with its editor.
   We recommend you give it a try, as it will most likely save you time in the long term.
   There are no plans to make Godot usable as a library, as it would make the rest of the engine more convoluted and difficult to use for casual users.

   If you want to use a rendering library, look into using an established rendering engine instead. 
   Keep in mind rendering engines usually have smaller communities compared to Godot. 
   This will make it more difficult to find answers to your questions.

*(* **Note:** *If a sentence ends with an aside in parentheses, add it to a new line as well)*

We do this as a tradeoff between having a line length limit *(Causing a seaming unnecessary amount of hassle)* and having not having a limit at all. 
*(Witch can be annoying to people without automatic wordwrap)*

Links and Headers
^^^^^^^^^^^^^^^^^

In our docs a **Header 1** is used for the title of an :ref:`article <yverb-article>`.
Titles should occur at the start, however warnings an notes may appear before hand.

All titles should include a ``ref`` link above for easy linking:

.. code-block:: rst

   .. _ydoc-contributing-docs:

   General Documentation (Article) Writing
   =======================================

We do *mostly* follow a small rule set to naming our ``ref`` s to avoid collisions:

 1. Prefix with ``ydoc`` *(This means* **Y** *omi* **Doc** *umentation and is used to avoid collisions with Godot's* ``ref`` *s)*
 2. Name the location *(This is usually the* **parent folder's** *name)*
 3. Header "name" *(This can just be the header name, or something slimmer, like* ``general-documentation`` *->* ``docs`` *)*

Also when ``:ref:``-ing another :ref:`article <yverb-article>`, we recommend adding a display name as to not interrupt the follow of the sentence, however **NEVER** just use the word *"here"* as a display name!

**DON'T:**

.. code-block:: rst

    * Haven't made a Mod before? Get Started :ref:`here <ydoc-tutorial-start>`!
    * Have a question or wanna chat? Join our :ref:`ydoc-community-channels`!

   .. Second bullet's ref resolves to "Join our Community Channels" witch is... *fine* but not ideal...

**DO:**

.. code-block:: rst

    * Haven't made a Mod before? :ref:`Get Started here <ydoc-tutorial-start>`!
    * Have a question or wanna chat? Join our :ref:`Community <ydoc-community-channels>`!

Media
^^^^^

All media *(ie. Images, Audio, Video, etc)* are stored *flat* in the ``_assets`` directory.
This means the main organizer is each file's name. 
Because of this we have a simple way to name media files:

    ``[concise-page-name-or-category]-[usage_index]``

    **eg:**

    ``contributing-classes-2.png``
    ``meme-0.gif``

Now to clarify, the first part is the page/category name of the media.
Normally, just the *page's concise name* *(or* **ID** *)* but if it is meant to be used across documents, a more appropriate *category name* should be chosen.

Usage index starts at 1, and indicates how far down the first occurrence of the media is used.
If it is used across multiple pages, then just increment it for each new entry into the category.

The reasoning for this, is to keep imitate the *"figure __."* type of naming style scientific papers use. It also makes it easy to both add and locate a piece of media, without having a maze of nested folders that may only store a single image.

Verbiage
^^^^^^^^

You may want to use words that may not be common knowledge to your reader, or is a acronym the community uses.
Now if this is the case, you may want to consider adding it to the :ref:`ydoc-community-verbiage` document.
Now before adding something to the document, consider these 2 questions:

 1. Is this a word/acronym used in casual community conversations?
 2. Would a new player not understand what it means? *(New player, as in played for 1-2 hours)*
 3. Will this word/acronym be used outside of my document or tutorial?
 4. Is this a word/acronym they could find an accurate meaning for in a Dictionary?

If you answered **Yes** to 1. or 3. *(and not 4.)*, feel free to add it!

If you only answered **Yes** to 2, and *No* on 1. and 3., then it would be best to just define your word in your own :ref:`article <yverb-article>`.

If you answered **Yes** to 4. *(Even if you said* **Yes** *to the others)* you should most likely just chose the previous option, or just not define it at all.
Allow the reader find the meaning themselves.

Small Formatting Styling
^^^^^^^^^^^^^^^^^^^^^^^^

Here are some personal things the original writer liked to do, but won't contributors be *"graded"* on:

 * Surrounding parenthetical with italics
 * Using ``*`` as the unordered list Prefix
 * Adding a space before every bullet in a list
 * Uses a single dash to indicate an em-dash *(Because of the stigma of em-dashes being related to AI)*
