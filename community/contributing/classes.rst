.. _ydoc-contributing-classes:

Writing Class Reference Documentation
=====================================

.. include:: /_snippets/ai-warning.rst

.. include:: /_snippets/new-contrib.rst

Class Reference Goals
---------------------

When writing a class reference, the following goals should be remembered:

 * :ref:`Class References <ydoc-class-reference>` should to **INFORM** the reader
 * After that, our secondary goal is to keep it accessible *(Like the* :ref:`Article (Documentation) Goals <ydoc-contributing-docs-goals>` *)*

The reason why this should be is because, most *Modders*, when they check a :ref:`class reference <ydoc-class-reference>` most likely already know how to use it, they just need a refresher on the specifics, so we *#1* focus on that.

We shouldn't try to hard to teach them *how to use it* as that is what the **Tutorials** are for, but we should try to make it easier to understand for *new Modders* to understand, secondarily.

.. rst-class:: make-accordion

Where are the Class files?
--------------------------

If you ever tried to edit a :ref:`class reference file <ydoc-class-reference>` you may have noticed the following comment:

.. literalinclude:: /_templates/class.rst.j2
   :language: rst
   :lines: 6-8

Now this is here because as stated in the lines above, you should not edit those files directly as they are generated from our tool script, ``make_rst.py``.

Now you may be wondering:

    *"Well if I cant edit the reference files there...* **Where do I edit them?** *"*

Well, they are actually placed in the ``classes`` folder, in the more accessible `TOML <https://toml.io/en/>`_ configuration file format.
*(mirroring* `Godot <https://github.com/godotengine/godot/tree/master/doc/classes>`_ *)*

We did this to make it easier to manually *(and programmatically)* read and write the :ref:`class references <ydoc-class-reference>`. 
We also did this to make it extremely easy for us to keep utmost consistency with the layout of each file, making it as *easy as possible* to **quickly** find the item you are looking for.

.. rst-class:: make-accordion

TOML Specification
^^^^^^^^^^^^^^^^^^

Now we do have a specific layout, and set of ``TOML`` fields you must follow to keep it valid.

----

Class Data (Header)
"""""""""""""""""""

.. literalinclude:: /classes/BaseObj.toml
   :language: toml
   :lines: 1-12

+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field           | Type                   | Description                                                                                                                                                                   |
+=================+========================+===============================================================================================================================================================================+
| ``verstion``    | ``str``                | YOMI Version.                                                                                                                                                                 |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``updated``     | ``str``                | Last updated date *(* ``YEAR-MM-DD`` *)*.                                                                                                                                     |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``name``        | ``str (optional)``     | The internal class's name.                                                                                                                                                    |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``desc``        | ``str (optional)``     | The description for the class. Has :ref:`BBCode capabilities <ydoc-contributing-classes-bbcode>`. *(Defaults to:* ``No description provided.`` *)*                            |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``category``    | ``str``                | The sidebar category's name.                                                                                                                                                  |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``inherits``    | ``str (optional)``     | The internal class it inherits from *(either unique name, or its script path)*.                                                                                               |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``script_path`` | ``str``                | The `Godot Resource Path <https://docs.godotengine.org/en/3.5/tutorials/io/data_paths.html>`_ for the actual script defining the class.                                       |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``scene_path``  | ``str (optional)``     | The `Godot Resource Path <https://docs.godotengine.org/en/3.5/tutorials/io/data_paths.html>`_ for the defining scene that the script resides in *(or just the parent scene)*. |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_ref``        | ``str (optional)``     | The raw `Sphinx Reference <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_ to use when linking.                                                                |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                                                                                                          |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``signals``     | ``mapping (optional)`` | A mapping of ``name (str)`` to :ref:`ydoc-contributing-classes-toml-signal`.                                                                                                  |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``constants``   | ``mapping (optional)`` | A mapping of ``name (str)`` to :ref:`ydoc-contributing-classes-toml-constant`.                                                                                                |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``properties``  | ``mapping (optional)`` | A mapping of ``name (str)`` to :ref:`ydoc-contributing-classes-toml-property`.                                                                                                |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``methods``     | ``mapping (optional)`` | A mapping of ``name (str)`` to :ref:`ydoc-contributing-classes-toml-method`.                                                                                                  |
+-----------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

----

.. _ydoc-contributing-classes-toml-signal:

Signal Data
"""""""""""

.. literalinclude:: /classes/Fighter.toml
   :language: toml
   :lines: 10-11

+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Field        | Type                   | Description                                                                                                                                         |
+==============+========================+=====================================================================================================================================================+
| ``desc``     | ``str (optional)``     | The description for the signal. Has :ref:`BBCode capabilities <ydoc-contributing-classes-bbcode>`. *(Defaults to:* ``No description provided.`` *)* |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_ref``     | ``str (optional)``     | The raw `Sphinx Reference <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_ to use when linking.                                      |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                                                                             |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| ``params``   | ``mapping (optional)`` | A mapping of ``name (str)`` to :ref:`ydoc-contributing-classes-toml-params`.                                                                        |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+

----

.. _ydoc-contributing-classes-toml-constant:

Constant Data
"""""""""""""

.. literalinclude:: /classes/Fighter.toml
   :language: toml
   :lines: 107-110

+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field        | Type                   | Description                                                                                                                                           |
+==============+========================+=======================================================================================================================================================+
| ``type``     | ``str``                | The datatype used for the constant. *(Whether a* :ref:`Godot Class/Type <doc_class_reference>` *or* :ref:`one of Ours <ydoc-class-reference>` *)*     |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``value``    | ``str``                | The chosen value for the constant.                                                                                                                    |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``desc``     | ``str (optional)``     | The description for the constant. Has :ref:`BBCode capabilities <ydoc-contributing-classes-bbcode>`. *(Defaults to:* ``No description provided.`` *)* |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_ref``     | ``str (optional)``     | The raw `Sphinx Reference <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_ to use when linking.                                        |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+

----

.. _ydoc-contributing-classes-toml-property:

Property Data
"""""""""""""

.. TODO: Should probably swap to using raw code blocks and not linking

.. literalinclude:: /classes/Fighter.toml
   :language: toml
   :lines: 381-384

+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field        | Type                   | Description                                                                                                                                           |
+==============+========================+=======================================================================================================================================================+
| ``export``   | ``bool (optional)``    | Flag for if the property is exported to the Godot Proprieties menu.                                                                                   |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``onready``  | ``bool (optional)``    | Flag for if the property is defined, right as the :ref:`_ready() <class_Node_method__ready>` signal is called.                                        |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``type``     | ``str``                | The datatype used for the property. *(Whether a* :ref:`Godot Class/Type <doc_class_reference>` *or* :ref:`one of Ours <ydoc-class-reference>` *)*     |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``value``    | ``str (optional)``     | The chosen value for the property.                                                                                                                    |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``desc``     | ``str (optional)``     | The description for the property. Has :ref:`BBCode capabilities <ydoc-contributing-classes-bbcode>`. *(Defaults to:* ``No description provided.`` *)* |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_ref``     | ``str (optional)``     | The raw `Sphinx Reference <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_ to use when linking.                                        |
+--------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+

----

.. _ydoc-contributing-classes-toml-method:

Method Data
"""""""""""

.. literalinclude:: /classes/BaseObj.toml
   :language: toml
   :lines: 1049-1051

.. TODO: Should probably swap to using raw code blocks and not linking

+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Field        | Type                   | Description                                                                                                                                         |
+==============+========================+=====================================================================================================================================================+
| ``type``     | ``str (optional)``     | The return datatype of the method. *(Whether a* :ref:`Godot Class/Type <doc_class_reference>` *or* :ref:`one of Ours <ydoc-class-reference>` *)*    |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| ``desc``     | ``str (optional)``     | The description for the method. Has :ref:`BBCode capabilities <ydoc-contributing-classes-bbcode>`. *(Defaults to:* ``No description provided.`` *)* |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_ref``     | ``str (optional)``     | The raw `Sphinx Reference <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_ to use when linking.                                      |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                                                                             |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| ``params``   | ``mapping (optional)`` | A mapping of ``name (str)`` to :ref:`ydoc-contributing-classes-toml-params`.                                                                        |
+--------------+------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+

----

.. _ydoc-contributing-classes-toml-params:

Parameter Data
""""""""""""""

.. literalinclude:: /classes/BaseObj.toml
   :language: toml
   :lines: 1053-1063

+------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field      | Type               | Description                                                                                                                                            |
+============+====================+========================================================================================================================================================+
| ``type``   | ``str (optional)`` | The datatype for the parameter. *(Whether a* :ref:`Godot Class/Type <doc_class_reference>` *or* :ref:`one of Ours <ydoc-class-reference>` *)*          |
+------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``value``  | ``str (optional)`` | The default value for the parameter.                                                                                                                   |
+------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``desc``   | ``str (optional)`` | The description for the parameter. Has :ref:`BBCode capabilities <ydoc-contributing-classes-bbcode>`. *(Defaults to:* ``No description provided.`` *)* |
+------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_ref``   | ``str (optional)`` | The raw `Sphinx Reference <https://www.sphinx-doc.org/en/master/usage/referencing.html>`_ to use when linking.                                         |
+------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``_order`` | ``int``            | The location of the parameter in the above **function**. *(Optional, if only 1 parameter)*                                                             |
+------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+

----

.. rst-class:: make-accordion

.. _ydoc-contributing-classes-bbcode:

BBCode Tags
^^^^^^^^^^^

When adding/modifying the ``desc`` field of any *item*, we have an `BBCode <https://docs.godotengine.org/en/stable/tutorials/ui/bbcode_in_richtextlabel.html>`_ parsing layer on top to make adding styling easier.

Here is a list of ``BBCode``-*like* tags we have access to:

Custom Tags
"""""""""""

.. rst-class:: tag-def-table

.. list-table::
   :width: 100%
   :widths: 35 45 20
   :header-rows: 1

   * - Tag
     - Usage
     - Result

   * - | **Reference Link**:
       | Create either a line to a class, signal,
       | constant,property, or method in this,
       | or another class.
       |
       | You can also set display text with
       | the ``|`` symbol.
     - | *(Current item:* :ref:`BaseObj.apply_forces()<class_baseobj_method_apply_forces>` *)*
       | ``[[]]``
       | ``[[class|This class]]``
       | ``[[class Fighter]]``
       | ``[[sig got_hit]]``
       | ``[[sig Fighter.parried]]``
       | ``[[const max_rumble]]``
       | ``[[const Utils.constant_dirs|Directions]]``
       | ``[[prop invulnerable]]``
       | ``[[prop ObjectState.anim_length]]``
       | ``[[meth apply_force]]``
       | ``[[meth FixedMath.rotate_vec|Rotate fixed Vector]]``
       | ``[[ref class-hitbox-property-hhit-particle|^Hitbox.HIT_PARTICLE]]``
     - |  :ref:`^BaseObj<class_baseobj>` 
       |  :ref:`This class<class_baseobj>` 
       |  :ref:`^Fighter<class_fighter>` 
       |  :ref:`^got_hit()<class_baseobj_signal_got_hit>`
       |  :ref:`^Fighter.parried()<class_fighter_signal_parried>`
       |  :ref:`^max_rumble<class_baseobj_constant_max_rumble>`
       |  :ref:`Directions<class_utils_constant_dirs>`
       |  :ref:`^invulnerable<class_baseobj_property_invulnerable>`
       |  :ref:`^ObjectState.anim_length<class_objectstate_property_anim_length>`
       |  :ref:`^apply_force()<class_baseobj_method_apply_force>`
       |  :ref:`Rotate fixed Vector<class_fixedmath_method_rotate_vec>`
       |  :ref:`^Hitbox.HIT_PARTICLE<class-hitbox-property-hhit-particle>`

   * - | **Documentation Only**:
       | Anything between *should* only be
       | shown when read by these docs,
       | and hidden in other external
       | locations.
     - ``Hello everyone! [docs](Secret docs message)[/docs]``
     - | ``In Docs:`` Hello everyone! (Secret docs message)
       | ``Externally:`` Hello everyone!

   * - | **External Only**:
       | Anything between *should* only be
       | shown when read in external
       | locations,and hidden in these
       | current docs.
     - ``Hello everyone! [external](Secret external message)[/external]``
     - | ``In Docs:`` Hello everyone!
       | ``Externally:`` Hello everyone! (Secret external message)

   * - | **Raw**:
       | Anything between gets kept as raw
       | ``RST``.
     - | ``Oh! Look at this button =o``
       |
       | ``[raw]``
       | ``.. raw:: html``
       |
       |      ``<button>I'm a Button :)</button>``
       |
       | ``[/raw]``
     - .. raw:: html
          
          Oh! Lock at this button =o

          <button>I'm a Button :)</button>

Richtext BBCode Subset
""""""""""""""""""""""

.. rst-class:: tag-def-table

.. list-table::
   :width: 100%
   :widths: 40 35 25
   :header-rows: 1

   * - Tag
     - Usage
     - Result

   * - | **Bold**:
       | Makes surrounded text bold.
     - ``Some [b]bolded[/b] text.``
     - Some **bolded** text.

   * - | **Italics**:
       | Makes surrounded text Italics.
     - ``Some [i]italicized[/i] text.``
     - Some *italicized* text.

   * - | **Underline**:
       | Adds an underline to surrounded text.
     - ``Some [u]underlined[/u] text.``
     - Some :underline:`underlined` text.

   * - | **Strikethrough**:
       | Adds a strikethrough to surrounding text.
     - ``Some [u]strikethroughed[/u] text.``
     - Some :strike:`strikethroughed` text.

   * - | **Paragraph**:
       | Forces text to be in a new paragraph.
       | Also has support for by adding the ``align`` field.
       | Supported alignment values are:
       | - ``left``/``l``
       | - ``center``/``c``
       | - ``right``/``r``
       | - ``fill``/``f``
     - ``[p align=l]Left,[/p][p align=c]Centered,[/p][p align=r]Right.[/p]``
     - .. container::

          .. container:: left

             Left,

          .. container:: center

             Centered,

          .. container:: right

             Right.

   * - | **Left**:
       | Makes the text horizontally left-aligned.
     - ``[left]Left Paragraph.[/left]``
     - .. container:: left

          Left Paragraph.

   * - | **Center**:
       | Makes the text horizontally centered.
     - ``[center]Center Paragraph.[/center]``
     - .. container:: center

          Centered Paragraph.

   * - | **Right**:
       | Makes the text horizontally right-aligned.
     - ``[right]Right Paragraph.[/right]``
     - .. container:: right

          Right Paragraph.

   * - | **Fill**:
       | Makes the text horizontally justified.
       | *(Trys to use the full width of available space)*
     - ``[fill]A longer paragraph that is filling the area.[/fill]``
     - .. container:: fill

          A longer paragraph that is filling the area.

   * - | **Line Break**:
       | Adds a line break in a text, without adding a new
       | paragraph.
     - ``This text is [br]split up into [br] multiple lines.``
     - | This text is
       | split up into
       | multiple lines.

   * - | **Horizontal Rule**:
       | Adds new a horizontal rule to separate content.
     - ``The text is split[hr]by a horizontal rule.``
     - .. image:: /assets/contributing-classes-1.png

   * - | **Indent**:
       | Causes any text inside to be indented to a
       | seemlier level to a list item.
     - ``[indent]Indented text[/indent]``
     -    Indented text

   * - | **Code**:
       | Makes surrounding text monospaced, and if
       | multiline adds syntax hightailing for the
       | chosen language.
     - | ``Some inline [code]code[/code] formatting.``
       | 
       | ``[code=gdscript]``
       | ``# Some example gdscript``
       | ``extends Node``
       | 
       | ``func _ready():``
       |     ``print("Hello Documentation!")``
     - .. image:: /assets/contributing-classes-2.png

   * - | **URL**:
       | Create a hyperlink to the inputted web url with an
       | optional display inner text.
     - ``This is a link to [url]https://example.com[/url]. And it links to [url=https://example.com]this website[/url].``
     - This is a link to `https://example.com <https://example.com>`_. And this is links to `this website <https://example.com>`_.

   * - | **Image**:
       | Embed an image onto the page, with optional width
       | and height. 
     - ``[img=96x32]/assets/meme-1.gif[/img]``
     - .. image:: /assets/meme-1.gif
          :width: 96px
          :height: 32px

   * - | **Tables**:
       | Creates a table with a defined number of columns.
       | Use the ``[cell]`` tag to define table cells.
     - ``[table=2][cell]A[/cell][cell]2[/cell][cell]by 2[/cell][cell]table[/cell][/table]``
     - .. image:: /assets/contributing-classes-3.png

   * - | **Unordered List**
       | Adds an unordered list, with each line representing
       | its own list item.
     - | ``[ul]``
       | ``Item 1``
       | ``Item 2``
       | ``Item 3``
       | ``[/ul]``
     - * Item 1
       * Item 2
       * Item 3

   * - | **Ordered List**
       | Adds an ordered list, with each line representing
       | its own list item.
     - | ``[ol]``
       | ``Item 1``
       | ``Item 2``
       | ``Item 3``
       | ``[/ol]``
     - 1. Item 1
       2. Item 2
       3. Item 3

   * - | **Left/Right Bracket**:
       | Adds ``[`` and ``]`` respectively.
       | Used to bypass BBCode parsing.
     - ``This text is [lb]b[rb]not bold[lb]\b[rb].``
     - This text is [b]not bold[\\b].

   * - | **Unicode Character**:
       | Adds any Unicode character with it's hexadecimal
       | UTF-32.
     - ``Look at this cool face [char=21A6] ( [char=0D26][char=0D4D][char=0D26][char=0D3F] [char=02D9][char=15DC][char=02D9] )``
     - Look at this cool face ↦ ( ദ്ദി ˙ᗜ˙ )

   * - | **Miscellaneous Unicode**:
       | A bunch of miscellaneous tags that get
       | automatically converted into useful unicode
       | control characters.
     - * ``[lrm]`` left-to-right mark
       * ``[rlm]`` right-to-left mark
       * ``[lre]`` left-to-right embedding
       * ``[rle]`` right-to-left embedding
       * ``[lro]`` left-to-right override
       * ``[rlo]`` right-to-left override
       * ``[lri]`` left-to-right isolate
       * ``[rli]`` right-to-left isolate
       * ``[pdf]`` pop directional formatting
     - * ``[alm]`` Arabic letter mark
       * ``[fsi]`` first strong isolate
       * ``[pdi]`` pop directional isolate
       * ``[zwj]`` zero-width joiner
       * ``[zwnj]`` zero-width non-joiner
       * ``[wj]`` word joiner
       * ``[shy]`` soft hyphen

Guidelines
----------

Guidelines to use when writing a :ref:`Class's Reference <ydoc-class-reference>`.

These are some of the rules we like to follow when contributing to this project's :ref:`Class Reference <ydoc-class-reference>` files. If you want to edit a :ref:`article <yverb-article>` file, read :ref:`ydoc-contributing-docs` instead.

To start off, we recommend you reading both the Godot :ref:`doc_content_guidelines` and :ref:`doc_docs_writing_guidelines` as those are the biases for our guidelines.
Then we recommend reading the :ref:`General Documentation Guidelines <ydoc-contributing-docs-guidelines>` as most are applicable here as well.

.. include:: /_snippets/guideline-note.rst
