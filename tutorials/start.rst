.. _ydoc-tutorial-start:

Getting Started
===============

So you wanna make you first :ref:`YOMI Hustle <yverb-yomih>` mod, do ya?
Well hold your horses bucko, you got to :ref:`setup your environment <ydoc-tutorial-setup>` first.

.. TODO: Use tabs to split versions

.. _ydoc-tutorial-setup:

Setup
-----

.. tip:: Setup instructions are text and image based.
         Below is a Youtube video, if you would like to watch one instead.

         .. figure:: https://img.youtube.com/vi/lfAeGR6jasw/maxresdefault.jpg
            :width: 512
            :alt: Watch the "YomiHustle Tutorials - Part 1 - Setup - [The Beeg Series] - (No Coding Series)" by `@Nuion on Youtube <https://www.youtube.com/@Nuion>`_!
            :target: https://www.youtube.com/watch?v=lfAeGR6jasw

            **YomiHustle Tutorials - Part 1 - Setup - [The Beeg Series] - (No Coding Series)**

.. rst-class:: make-accordion

Prerequisites
^^^^^^^^^^^^^

Below are some prerequisite you need to have downloaded and installed to start modding:

 * `Your Only Move is Hustle (Steam Version) <https://store.steampowered.com/app/2212330/Your_Only_Move_Is_HUSTLE/>`_ 
 * `Godot Steam 3.5.1 <https://codeberg.org/godotsteam/godotsteam/releases/tag/g351-s155-gs3184>`_
 * `GDSDecomp <https://github.com/GDRETools/gdsdecomp/releases>`_

If already have those installed, you can :ref:`skip the following<ydoc-tutorial-setup-decomp>`.

.. rst-class:: make-accordion close

Installing Godot Steam 3.5.1
""""""""""""""""""""""""""""

These are the instructions for installing Godot Steam, a Godot fork that has steam combatably built in.
It also includes raw `Steamworks SDK <https://partner.steamgames.com/doc/sdk>`_ file witch is required for :ref:`YOMIH <yverb-yomih>` to work.

In our case :ref:`YOMIH <yverb-yomih>` specifically uses version **3.5.1** of this program, so we will be installing that.

**Windows:**

 1. **Download** `Godot Steam 3.5.1 <https://codeberg.org/godotsteam/godotsteam/releases/tag/g351-s155-gs3184>`_ :download:`64bit <https://codeberg.org/godotsteam/godotsteam/releases/download/g351-s155-gs3184/win64-g351-s155-gs3184.zip>`   *(or* :download:`32bit <https://codeberg.org/godotsteam/godotsteam/releases/download/g351-s155-gs3184/win32-g351-s155-gs3184.zip>`   *)* ``.zip`` **into your** ``Downloads`` **folder.**

 2. **Make a new folder to store** *Godot Steam* **in.**
    *(Name it something like* ``yomi-godot`` *as this will most likely only be used for modding)*
   
    *Godot Steam* is a `portable application <https://www.youtube.com/watch?v=ammHv71hmso>`_ it is recommended to put it in your portable installation folder, if you have one.
    If you don't have one, we highly recommend making one, as you will come across applications like this pretty often.
   
    *(Personally I just have a folder named* ``Programs`` *in my* ``Desktop`` to place them in)*

 3. **Extract the *Godot Steam* ``.zip`` into the new folder.**

 4. **Run the** ``windows-351-editor-64bit.exe`` **file.**
   
    This will the executable you open to run the *Godot Steam Editor*.
    *(ie. What you will open to actually mod)*

 5. *(Optional)* **Create a shortcut to** ``windows-351-editor-64bit.exe`` **on your** ``Desktop``.

    Name it ``YOMI Godot`` if you want.

    .. tip::

       Here is an icon for the shortcut you can :download:`download </assets/downloads/yomi-godot.ico>` for the shortcut.

       .. image:: /assets/downloads/yomi-godot.ico
          :width: 64

**Linux**

 1. **Download** `Godot Steam 3.5.1 <https://codeberg.org/godotsteam/godotsteam/releases/tag/g351-s155-gs3184>`_ :download:`Linux <https://codeberg.org/godotsteam/godotsteam/releases/download/g351-s155-gs3184/linux64-g351-s155-gs3184.zip>` ``.zip`` **into your** *Downloads* **directory.**

    .. code-block:: bash

       curl --output-dir ~/Downloads/ -o https://codeberg.org/godotsteam/godotsteam/releases/download/g351-s155-gs3184/linux64-g351-s155-gs3184.zip

 2. **Make a new directory to store** *Godot Steam* **in.**
    *(Name it something like* ``yomi-godot`` *as this will most likely only be used for modding)*
   
    *Godot Steam* is a `portable application <https://www.youtube.com/watch?v=ammHv71hmso>`_ it is recommended to put it in your portable installation folder, if you have one.
    If you don't have one, we highly recommend making one, as you will come across applications like this pretty often.
   
    *(Personally I just have a directory named* ``Programs`` *in* ``~/Documents`` *to place them in)*
  
    .. important:: Set ``YOMI_GODOT_DIR=`` to the full path you want to store *Godot Steam* inside.
                  *(Path starting from root)*

    .. code-block:: bash

       YOMI_GODOT_DIR="!Enter path here!"
       mkdir -p "$YOMI_GODOT_DIR"


 3. **Extract the** *Godot Steam* ``.zip`` **into the new directory.**

    .. code-block:: bash

       unzip ~/Downloads/linux64-g351-s155-gs3184.zip -d "$YOMI_GODOT_DIR"

 4. **Give executable permissions to ``linux-351-editor.64`` and run it.**

    This will the executable you open to run the *Godot Steam Editor*.
    *(ie. What you will open to actually mod)*
   
    .. warning:: Make sure to run it in the same directory as ``yomi-godot`` as the editor uses your **current working directory** *(* ``pwd`` *)* to find ``libsteam_api.so``.

    .. code-block:: bash

       cd "$YOMI_GODOT_DIR""
       chmod +x linux-351-editor.64
       ./linux-351-editor.64
 
 5. *(Optional)* **Create a shortcut to** ``windows-351-editor-64bit.exe`` **on your** ``Desktop``.

    For more exact steps, read :ref:`ydoc-tutorial-setup-extra-linux`.

**Mac:**

.. note:: *Instructions, Coming Soon*

.. rst-class:: make-accordion close

.. _ydoc-tutorial-setup-install-decomp:

Installing GDSDecomp
""""""""""""""""""""

**Windows:**

 1. **Find and Download the** `latest GDSDecomp <https://github.com/GDRETools/gdsdecomp/releases>`_ ``.zip`` *(* :download:`Windows v2.6.0 Download <https://github.com/GDRETools/gdsdecomp/releases/download/v2.6.0/GDRE_tools-v2.6.0-windows.zip>`  *)* **into your** ``Downloads`` **folder.**

 2. **Make a new folder to store** *GDSDecomp* **in.**
    *(You technically don't have to, but personally i would)*

    *GDSDecomp* is a `portable application <https://www.youtube.com/watch?v=ammHv71hmso>`_ it is recommended to put it in your portable installation folder, if you have one.
    If you don't have one, we highly recommend making one, as you will come across applications like this pretty often.
   
    *(Personally I just have a folder named* ``Programs`` *in my* ``Desktop`` *to place them in)*


 3. **Extract the** *GDSDecomp* ``.zip`` **into the new folder.**

 4. **Run** ``gdre_tools.x86_64``.
    
    .. tip:: Make sure to remember the location of this executable.
             You will use it in the :ref:`ydoc-tutorial-setup-decomp` Section.

**Linux:**

 1. **Find and Download the** `latest GDSDecomp <https://github.com/GDRETools/gdsdecomp/releases>`_ ``.zip`` *(* :download:`Linux v2.6.0 Download <https://github.com/GDRETools/gdsdecomp/releases/download/v2.6.0/GDRE_tools-v2.6.0-linux.zip>`  *)* **into your** *Downloads* **directory.**

    .. code-block:: bash

       curl --output-dir ~/Downloads/ -o https://github.com/GDRETools/gdsdecomp/releases/download/v2.6.0/GDRE_tools-v2.6.0-linux.zip

 2. **Make a new directory to store** *GDSDecomp* **in.**
    *(You technically don't have to, but personally i would)*

    *GDSDecomp* is a `portable application <https://www.youtube.com/watch?v=ammHv71hmso>`_ it is recommended to put it in your portable installation folder, if you have one.
    If you don't have one, we highly recommend making one, as you will come across applications like this pretty often.
   
    *(Personally I just have a directory named* ``Programs`` *in* ``~/Documents`` *to place them in)*

    .. important:: Set ``GDSDECOMP_DIR=`` to the full path you want to store *GDSDecomp* inside.
                  *(Path starting from root)*

    .. code-block:: bash

       GDSDECOMP_DIR="!Enter path here!"
       mkdir -p "$GDSDECOMP_DIR"

 3. **Extract the** *GDSDecomp* ``.zip`` **into the new folder.**

    .. code-block:: bash

       unzip ~/Downloads/GDRE_tools-v2.6.0-linux.zip -d "$GDSDECOMP_DIR"

 4. **Give executable permissions to ``gdre_tools.x86_64`` and run it.**
    
    .. tip:: Make sure to remember the location of this executable.
             You will use it in the :ref:`ydoc-tutorial-setup-decomp` Section.

    .. code-block:: bash

       cd "$GDSDECOMP_DIR""
       chmod +x gdre_tools.x86_64
       ./linux-351-editor.64

**Mac:**

.. note:: *Instructions, Coming Soon*

----

.. rst-class:: make-accordion

.. _ydoc-tutorial-setup-decomp:

Decompiling YOMI Hustle
^^^^^^^^^^^^^^^^^^^^^^^

.. warning:: The below steps do *require* you to know the *folder path* to where :ref:`YOMI Hustle <yverb-yomih>` is installed.
             If you don't know, find it by following :ref:`these steps <ydoc-tutorial-setup-decomp-path>`:

Here is how you can decompile **your** *(yes, YOUR)* install of :ref:`YOMI Hustle <yverb-yomih>`.


.. warning:: Each time :ref:`YOMI Hustle <yverb-yomih>` updates, you **may** need to do this process again!
             *(Unless you want outdated mods)*

.. tip:: If you want to skip this, you can download the official source code at https://github.com/uzkbwza/hustle.

1. **Create a new folder for where you want to store the decompiled code of** :ref:`YOMI Hustle <yverb-yomih>` **in.**

   .. note:: Remember the **full path** of this location, as it will be used in *step 4.*

2. **Open the** *GDSDecomp* **executable.**

   *(Previously remembered from the* :ref:`ydoc-tutorial-setup-install-decomp` *Section)*

3. **Select** *RE Tools* **then** *Recover Project...* .

   .. image:: /assets/tutorials-start-1.png
      :width: 512

   .. YES, i know its slightly outdated, but its mostly the same so i don't care... AND YOU SHOULDN'T EITHER!!1! >:(

4. **Navigate to/paste the folder location of your** :ref:`YOMI Hustle <yverb-yomih>` **installation, and select the file named**  ``YourOnlyMoveIsHUSTLE.pck``.
  
   .. FIXME: Use Windows Screenshots instead.
 
   .. image:: /assets/tutorials-start-2.png
      :width: 512

5. **Wait for it to load, click the** *Select* **button near the bottom of the screen, then navigate to/paste the folder you CHOSE to store the decompiled code of** :ref:`YOMI Hustle <yverb-yomih>` **in. Finally,** *Open* **it and hit** *Extract*.
  
   .. FIXME: Fix annotation issue OR...
   .. FIXME: Just use Windows screenshot with new annotations

   .. image:: /assets/tutorials-start-3.png
      :width: 512

6. Wait a while as the decompilation process runs. You may see warning or errors popup in the log area you can ignore them.
   **Once the popup appers, hit** *OK* **and close** *GDSDecomp*.
   
   .. XXX: Maybe we need a checksum check?? im not sure...
   .. tip:: If you want to varify your decompilation, you can do that by opening the folder you chose to store the compilation in, and checking to see if everything looks good.

   .. image:: /assets/tutorials-start-4.png
      :width: 512

7. **Navigate back to the location of your** :ref:`YOMI Hustle <yverb-yomih>` **installation, open the** ``lib`` folder, and copy the file named ``tbfg.dll``.
  
  .. note:: On *Linux,* ``tbfg.dll`` is actually named ``tbfg.so``.

  .. warning:: If you forget to do this, the game will crash as soon as you try to run it.
  
  .. XXX: Maybe move this to verbiage.rst? im not fully sure on that...
  ``tbfg`` *stands for* **Turn Based Fighting Game**.

8. **Navigate back to the location of the folder you chose to store the decompiled code of** :ref:`YOMI Hustle <yverb-yomih>` **in. Then open the** ``lib`` **folder in there, and paste** ``tbfg`` **in there.**

9. *Now* **Navigate back to the location of your** *GDSDecomp* **installation, and copy the file named** ``steam_api64.dll`` *(or* ``steam_api32.dll`` *in the* **32bit** *version) and copy it.*

  .. note:: On *Linux,* ``steam_api64.dll`` is actually named ``libsteam_api.so``.

  .. warning:: If you forget to do this, running the project will do nothing and won't even give you an error message.
               Also hitting ``Quit to project list`` won't open the project list after quitting.

10. **Finally, navigate back to the decompiled code folder, and paste the** *steam* **library directly into the root of the project.**

**Congratulations!** You have successfully decompiled :ref:`YOMI Hustle <yverb-yomih>`. Now you can continue to :ref:`ydoc-tutorial-setup-godot`.

.. tip:: We recommended creating a copy of the decompilation folder, prefixing with the phrase ``-backup`` to backup your decompilation.

.. rst-class:: make-accordion close

.. _ydoc-tutorial-setup-decomp-path:

Find where YOMIH is Downloaded
""""""""""""""""""""""""""""""

 1. Open *Steam*.

 2. **Go to** ``Library`` **and select the game** *Your Only Move Is HUSTLE* **from the sidebar or shelf.**
    
    .. figure:: /assets/tutorials-start-5.png
       :width: 512

    .. figure:: /assets/tutorials-start-6.png
       :width: 512

 3. **Click the** *Settings Icon*, **then hover over** *Manage* **and click** *Browse local files*.

    .. figure:: /assets/tutorials-start-7.png
       :width: 512

 4. **Focus on the file Explorer window then copy the** *folder path* **from on the top bar.**
    
    .. list-table::
      :class: format-table column-equal
      :width: 100%
    
      * - .. figure:: /assets/tutorials-start-8-1.png

              Windows Screenshot of the Windows File Explore *(Cropped from* `@Nuion on Youtube <https://youtu.be/lfAeGR6jasw?t=34>`_ *).*
        - .. figure:: /assets/tutorials-start-8-2.png

              Linux Screenshot of `Dolphin File Explore <https://apps.kde.org/dolphin/>`_ on the `KDE Plasma Desktop environment <https://kde.org/plasma-desktop/>`_.

----

.. rst-class:: make-accordion

.. _ydoc-tutorial-setup-godot:

Setting up Godot
^^^^^^^^^^^^^^^^

 1. **Open the** *Godot Steam* **Editor executable.**

    .. note:: On Linux, you may be required to run ``"$YOMI_GODOT_DIR/linux-351-editor.64"`` in your terminal to get it to accually run.

 2. **Click the** *Import* **button on the sidebar, then navigate to/paste the folder path for your :ref`YOMI Hustle <yverb-yomih>` **decompilation. Finally click the** *Import & Edit* **button.**

    .. image:: /assets/tutorials-start-9.png
       :width: 512

After doing that, it should automatically show the splash screen and open the project.
*If it looks something like this you did everything correct:*

.. HEHE... i left a little sneakpeak to my future projects in this image :p
.. image:: /assets/tutorials-start-10.png

To open the Decompiled YOMI from now on, just select it from the **Project Manager** window, and click the *Edit* button on the sidebar.

.. image:: /assets/tutorials-start-11.png

.. tip:: Now if you want to make Mod development a little faster, you can install some of the :ref:`recommended plugins <ydoc-tutorial-setup-plugins>`.

   And if you want to streamline the launching process *(specifically on Linux)*, read :ref:`ydoc-tutorial-setup-extra-linux`.

----

.. rst-class:: make-accordion close

.. _ydoc-tutorial-setup-plugins:

Installing recommended Plugins (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below are some community recommended Godot plugin that you can install, to make modding easier.

.. FIXME: If these have Github direct download links, use them instead as discord cdn links are not permanent.
.. XXX: This will also eventually be moved into the community section, so plugin/mod devs can add there own docs
..
.. Also adding [REDACTED] here soon :D (hehe)
..

 * :download:`Draggable CollisionBoxes by @ramwould (v1.0.10) <https://cdn.discordapp.com/attachments/1480063313902833685/1513235697547476992/draggable_collisionbox_v1.0.10.zip?ex=6a5fae90&is=6a5e5d10&hm=5400be7b8725a80fe096483232b08b34cbed2e09b281d044599de4a253ceebac&>`  : Adds the ability to visually edit all types of Hitboxes with the mouse.
   *(just like any other Godot-native object)*
 * :download:`StateAnimSync by @ramwould (v1.1.2) <https://cdn.discordapp.com/attachments/1480063313902833685/1497967489437536366/state_anim_sync_v1.1.2.zip?ex=6a5f81f0&is=6a5e3070&hm=29a005137e468b51bd3905a77d5931b60e784cebdf2c35e6e14aa7f733055a4e&>`  : Makes Godot try to display the current states's animation frame onto your character in the editor.
 * :download:`CharStateEditor Fix by @ramwould (v1.3) <https://cdn.discordapp.com/attachments/1480063313902833685/1504703166820651128/CharStateEditor1738_v1.3.zip?ex=6a5f9f47&is=6a5e4dc7&hm=ad8ba7c3c3574782a3deac1fc4d9fc6dd3bb9dfe2fdbeb8963d8dbcf1aa3abd2&>`  : Fixes some bugs with the :ref:`Character State Editor <ydoc-tutorial-state-editor>`.
 * :download:`Limb Tagger Fix by @ramwould (1.2) <https://cdn.discordapp.com/attachments/1480063313902833685/1525292209526669390/limb_finder_1.2b.zip?ex=6a5f60d1&is=6a5e0f51&hm=f4f2725e9fc11ebff056f98b8a16a76894dc7e073f0aef776873eb8924fca360&>`

.. FIXME: UH IDK what this dose :sob:???? ^

How to install a plugin
"""""""""""""""""""""""

 1. **Download the plugin as a** ``.zip``
 2. **Move the** ``.zip`` *(* Cut [``Ctrl/Command+X``] *file, then paste* [``Ctrl/Command+P``] *at new location)* **to the** ``addons`` **folder in the :ref:`YOMI Hustle <yverb-yomih>` decompilation.**
 3. **Make a new folder in** ``addons`` **with the same name as the plugin's** ``.zip`` *(Without the ``.zip`` extension)* **and move the** ``.zip`` **in there.**

    .. I don't know why but I really like this analogy :)
    .. note:: Technically this isn't needed, but some ``.zip`` don't have an internal folder, so extacting can *"spill"* its contents everywhere.

 4. **Extract the zip into that folder**

    .. note:: Most likely there will be another folder inside.
              
              If this is the case, enter the folder, select all items index, move them to the parent folder, then delete the empty folder.
 5. **Open the** :ref:`YOMI Hustle <yverb-yomih>` **decompilation project in** *Godot Steam*.
 6. **Select** *Project > Project Settings* **On the top bar, then in the new window select the** *Plugins* **Tab, then make sure the new plugin has a checkmark on there row.**

    .. YOU WILL NEVER KNOW! NYEH HEH HEH HEEEEEH *cough x2* *wheez* *cough x3*...
    .. image:: /assets/tutorials-start-12.png

.. tip:: If you ever to to update a plugin, delete the plugin's folder, then follow steps 1-6.

----

.. rst-class:: make-accordion close

Extra setup (Optional)
^^^^^^^^^^^^^^^^^^^^^^

.. rst-class:: make-accordion close

.. _ydoc-tutorial-setup-extra-linux:

Speeding up Development with Linux
""""""""""""""""""""""""""""""""""

You can create a shortcut to automatically open the project on your *terminal* and the **Desktop** by following the below steps:
   
Creating shortcuts in Linux can be a little more confusing then in Windows.
Here is a mini tutorial on how to do so:
1. **Create the helper script.**

   First you will need to create a bash script in the editor of your choice.
   *This script will automatically open the** :ref:`YOMIH <yverb-yomih>` **decompiled project.**

   Name the file ``yomi-godot.sh``, and paste the following:

   .. code-block:: bash

      #!/bin/bash

      YOMIGDPATH="Enter full yomi-godot path"
      YOMIDECOMP="Enter full yomi-decomp path"

      cd $(dirname $YOMIGDPATH)
      $YOMIGDPATH --editor --path $YOMIDECOMP
  
   We now have to make sure it has the execute permission with the ``chmod``.

   .. code-block:: bash

      chmod +x yomi-godot.sh

   After that, move it to the ``yomi-godot`` path:

   .. code-block:: bash

      mv yomi-godot.sh $YOMI_GODOT_DIR

2. **Create the** ``.desktop`` **file.**

   In your text editor of choice, create a file called ``yomi-godot.desktop``.
    
   .. tip::
      
      Now if you don't know, ``.desktop`` is the file format used by most distros as what is essentially shortcuts on Linux *(specifically for applications)*.
      Whats nice is that the ``.desktop`` file is basically just a ``.cgf`` file, so we can vary easily modify it and write our own completely *from scratch*.

   .. important:: Paste the following, replacing all mentions of ``[YOMI_GODOT_DIR]`` with the full path for the directory storing *Godot Steam*. 

   .. code-block:: ini
    
      [Desktop Entry]
      Categories=Development
      Comment[en_US]=Godot Steam Engine 3.5.1
      Comment=Godot Steam Engine 3.5.1
      Encoding=UTF-8
      Exec=[YOMI_GODOT_DIR]/yomi-godot.sh
      GenericName[en_US]=
      GenericName=
      Icon=
      MimeType=
      Name[en_US]=YOMI Godot
      Name=YOMI Godot
      Path=[YOMI_GODOT_DIR]
      StartupNotify=true
      Terminal=true
      TerminalOptions=
      Type=Application

   .. tip::

      .. image:: /assets/downloads/yomi-godot.ico
        :width: 64

      If you want it to use the above **custom icon**, :download:`download it here </assets/downloads/yomi-godot.ico>` and place it into the ``yomi-godot`` directory.
      Then in ``yomi-godot.desktop``, Edit the ``Icon=`` line to be ``Icon=[YOMI_GODOT_DIR]/yomi-godot.ico`` instead.

   Now technically you can just move ``yomi-godot.desktop`` to your **Desktop** and it would work, however, continuing uses a better option.

3. **Add it to your user's system** ``applications``.

   In most Linux distros, you can add ``.desktop`` files to ``~/.local/share/applications/`` to get them to show up in system menus.

   .. code-block:: bash

      mv yomi-godot.desktop ~/.local/share/applications/
   
   After doing that, to make is show up on the **Desktop**, just create a `symbolic link <https://linuxvox.com/blog/what-are-symlinks-in-linux/#1-what-are-symbolic-links>` from it, to the **Desktop**.

   .. code-block:: bash

      ln -s ~/.local/share/applications/yomi-godot.desktop ~/Desktop/yomi-godot.desktop

   .. warning:: If you want to edit/copy/delete the shortcut, remember that this is a and that any actions you do to the one on the ``Desktop``, gets mirrored to the one in ``~/.local/share/applications/``.

               This can especially get confusing when trying to make a copy of the shortcut, as both the original, and the copy will link to the same file.
               *(Even if they have different names)*

               To fix this, make sure to make the copy inside of ``~/.local/share/applications/`` instead, then create a *new link* from there.


4. *(Super Optional)* **Link your script to the "``PATH``"**

   If you also want to be able to acces yomi-godot from the terminal, create a symbolic link from the script to ``~/.local/bin/`` with the file name ``yomi-godot``.
   *(No extension)*

   .. code-block:: bash

      ln -s "$YOMI_GODOT_DIR/yomi-godot.sh" ~/.local/bin/yomi-godot

   Then reload your terminal.

   Now you can run the command ``yomi-godot`` from anywhere and it will automatically start ``yomi-godot.sh``

   .. code-block:: bash

      [user@host]$ yomi-godot
      Godot Engine v3.5.1.stable.custom_build.6fed1ffa3 - https://godotengine.org
      Found discrete GPU, setting DRI_PRIME=1 to use it.
      Note: Set DRI_PRIME=0 in the environment to disable Godot from using the discrete GPU.
      OpenGL ES 3.0 Renderer: HAINAN (radeonsi, , ACO, DRM 2.51, 6.17.0-35-generic)
      Async. shader compilation: OFF
      ...

Next Steps
----------

Great job land-lubber, you have valiantly built a grand vessel to sail the *two seas* abroad, however a great parting is afoot.
Witch path will you voyage hence forth:

 * :doc:`character/index`
 * :doc:`mod/index`
