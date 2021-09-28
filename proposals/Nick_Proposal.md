Reuploading to this repository since it didnt seem to be noticed in my own repository.

Initial Proposal:
For this project I will be working with Steve Bush in order to learn more about the DMX-512 and attempt to integrate it into the overall class theme project.
 We will be working on the hardware aspect of the project, meaning we will be taking the binary representations of the music frequencies and running it through a Raspberry PI to translate those signals into voltage outputs to power different sets of devices to create the show.
 As of right now, our main task is to learn more about the use of a Raspberry PI in order to learn how it can be used to integrate with the other project groups to bring everything together.
 Once we learn more about the hardware, we can start to figure out how we will recieve and interpret the information provided by the other groups to create our desired output.

Proposal Update 10/19
The Raspberry PI will probably be too slow for our use, so we will need to figure out a way to transfer signal from the PI to an Arduino. The Arduino is able to operate at a faster baud rate, so we will be able to communicate with the DMX correctly. 
For the first part of the project, we have decided to focus on the communication between the devices to ensure that the system can work, before we get too far into the details of how the show will run.

    We have decided to split this into two separate parts.
        First, I will be working on the connection between a PC and the Pi in order to allow us to control the system remotely through ethernet. This will eliminate the need to have a mobile PC that is capable of running the software for the show
        Second, Steve will be working on the connection between the Pi and the Arduino to get them to work together.
