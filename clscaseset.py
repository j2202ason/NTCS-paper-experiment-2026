class DataExperiments:
    def __init__(self):
        pass

    def getdata(self,idx):
        self.data = [
        '''
Plasma cutting is a process that uses a high-velocity jet of ionized gas (i.e., plasma) to cut metal workpieces. To create plasma, an electric arc is struck between the electrode and the workpiece. The high-temperature plasma heats the workpiece, melting the metal. The high velocity plasma jet blows the molten metal away, thus cutting the workpiece. A significant problem with conventional plasma cutting is the wear of electrodes whose temperature can reach 3000◦C. Typically, the electrodes include a hafnium, or a zirconium, or a titanium insert. These materials are desired for their ability to withstand high temperatures, but are very costly and require frequent replacement. Cooling of the electrodes complicates the overall system and is only marginally effective.
        ''',
        '''
Self-unloading barges are often used in dam construction. The barge carries the bulk cargo (e.g., stones, pebbles, etc.) and is hauled by a tugboat to the place where the cargo should be unloaded (by turning the barge upside down). The heavy keel and the buoyancy force generate a moment, returning the empty barge to its upright position. The heavier the keel is, the faster the upturn, however the heavy keel reduces the weight-carrying capacity of the barge, which is an undesirable
effect.
        ''',
        '''
A conventional bench vise is designed to clamp parts of regular shapes. To clamp irregularly shaped parts, special jaws have to be installed. The fabrication of
such jaws is usually costly.
        ''',
        '''
A punch becomes disabled quickly during a cold punching (cutting out) of molybdenum parts for semiconductor devices. The “evident” source of trouble is the very hard molybdenum. Molybdenum cannot be replaced because it is the only material compatible with the semiconductor (the same thermal expansion coefficient). There are restrictions for the punch and die substitution also. But it cannot be allowed that this technical system does not work because assembly of the semiconductor devices is the main company business.
        ''',
        '''
Against the background of a need for more fuel efficient vehicles, auto manufacturers are urgently looking for ways to reduce vehicle weight. One area which is under active investigation is the use of aluminium body panels to replace steel. Indeed, some car manufacturers such as Audi and Jaguar are already using the technique on their more expensive models. In order to form a body panel,flat sheets of metal are fed from a stack of sheets into a press Steel sheets can be fed very quickly by this method – as fast as one every two seconds, but aluminium sheets can only be fed at a rate of 8 per minute. There are tried and tested methods to separate steel sheets using magnets but these don't work for aluminium because it is nonmagnetic. Also, the aluminium sheets are coated with a sticky oil film, which is needed for a previous process step and cannot be easily removed. The Nine Sigma RFP requested solutions which would allow a doubling of feed rate for aluminium sheets.        
        '''
        ]

        return self.data[idx]