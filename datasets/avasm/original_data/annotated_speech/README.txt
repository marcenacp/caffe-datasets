  ______________________________________________________
/|               The AVASM Dataset 1.0                  |\
/|        Audio Visual Acoustic Space Mapping           |\
/|           - annotated speech sounds -                |\
/|______________________________________________________|\
==========================================================

---------------------AUTHOR CONTACT-----------------------
Antoine Deleforge

INRIA Grenoble Rhone-Alpes
Perception Group
655 Avenue de l'Europe
38330 Montbonnot Saint-Martin
France

Tel: +33 (0)4 76 61 52 08

E-mail: Antoine.Deleforge@inria.fr


-------------------------WEBSITE--------------------------
http://perception.inrialpes.fr/~Deleforge/AVASM_Dataset/


-----------------------TERMS OF USE-----------------------
The AVASM dataset is freely accessible for scientific research purposes and for non-commercial applications. 


------------------------DESCRIPTION-----------------------
This folder contain 108 binaural recordings of a single static sound source emitting a random utterance from the TIMIT dataset [2]. in a real-world environmenet. The sound source is a standard loud-speaker manually placed in the binaural head environement. Each recorded recording is between 1 and 5 second long, and is annotated with the pixel position of the sound source in the camera field of view, as well as the index of the emitted sound.


-------------------------CONTENT--------------------------
====./pixel_positions====
	This file contains a 108 x 3 table of floats, mapping sound files to their corresponding 2D pixel location. For example, the line "42	226.19	278.534	" means that the sound named "42.wav" was recorded when the loud-speaker was at position (x-axis = 226.19, y-axis = 278.19) in the camera field of view, where the x-axis is horizontal from left to right, and the y-axis is vertical from top to bottom.

====./timit_indexes====
	This file contains a 108 x 2 table of integers, mapping sound files to their corresponding emitted TIMIT sound index. For example, the line "42    353  " means that the sound name "42.wav" correspond to the binaural recording of the sound indexed 353 in our TIMIT samples. Note that identical sounds have been emitted from different positions. The originally emitted sounds are not provided due to license issues.

====./Recorded/====
	This folder contains 108 binaural wav files named "k.wav" where k=1...108. They correspond to binaural recordings of a sound source placed at different position, and emitting a utterance from the TIMIT_normalized folder. More information can be found at [1].

--------------------------------------------------------------------------
[1] http://perception.inrialpes.fr/~Deleforge/AVASM_Dataset/setup.html.
[2] http://catalog.ldc.upenn.edu/LDC93S1


