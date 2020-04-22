import datetime
import uuid 

class PersonState:

    def __init__(self, state, year, month, day):
        self.status = False
        self.readAbleState = None
        self.isStateFrom = datetime.datetime(year, month, day)

    def __str__(self):
        return (str(self.readAbleState) + " since " + str(self.isStateFrom))

class PersonHasSymptom(PersonState):
    
    def __init__(self, state, year, month, day):
        print("PersonHasSymptom")
        super().__init__(state, year, month, day)
        self.readAbleState="Has Symptoms"
        

class PersonIsAffected(PersonState):
    
    def __init__(self, state, year, month, day):
        print("PersonIsAffected")
        super().__init__(state, year, month, day)
        self.readAbleState="Is Affected"
        

class PersonIsNotAffected(PersonState):
    
    def __init__(self, state, year, month, day):
        print("PersonIsNotAffected")
        super().__init__(state, year, month, day)
        self.readAbleState="Is Normal"
        


class Person:
     
    def __init__(self):
        self.locationHistory = dict()
        self.caution = "NORMAL"
        self.id = uuid.uuid1()
        status = False
        todayDate = datetime.date.today()
        self.state = PersonIsNotAffected(status, todayDate.year, todayDate.month, todayDate.day)

    def setCarefulCaution(self):
        self.caution = "CAREFUL"

    def setIsolateCaution(self):
        self.caution = "ISOLATE"

    def hasSymptom(self, year, month, day):
        status = True
        self.state =  PersonHasSymptom(status, year, month, day)

    def isAffected(self, year, month, day):
        status = True
        self.state =  PersonIsAffected(status, year, month, day)


    def visitsLocation(self, location, year, month, day):
        #visitEvent = VisitEvent(location, year, month, day)
        #self.locationHistory.append(visitEvent)

        date = datetime.date(year, month,day)
        self.locationHistory[date]=location


    def getVisits(self):
        return self.locationHistory

    def getVisitLocationForDate(self, date):
        print("getVisitLocationForDate******")
        print(self.id)
        print(self.locationHistory)
        print(date)
        if date in self.locationHistory:
            return self.locationHistory[date]
        else:
            return None


    def printVisits(self):
        for visitEvent in self.locationHistory:
            print("On " + str(visitEvent) + ", visited " + str(self.locationHistory[visitEvent]))



    def __str__(self):
        if(self.id!=None):
            return (str(self.id) + " : " + str(self.state) + ", they should remain " + str(self.caution))
        else:
            return (self.state)
  

class Location:
    latitudeX = None
    latitudeY = None
    longitudeX = None
    longitudeY = None

    def __init__(self,latX, latY, longX, longY):
        self.latitudeX=latX
        self.longitudeX=longX
        self.latitudeY=latY
        self.longitudeY=longY


    def __str__(self):
        return str("Lat : " + str(self.latitudeX) + ","+ str(self.latitudeY) + " Long : " + str(self.longitudeX)+ ","+ str(self.longitudeY))


class CrossPath:

    @staticmethod
    def checkIfPathCrossed(person0, person1, dateOfEvent):
        print("checkIfPathCrossed")
        print(person0.getVisits())
        print(person1.getVisits())
        #Check if their location histories have a match 
        isPathCrossed = False 
        location0 = person0.getVisitLocationForDate(dateOfEvent)
        print(str(person0) + " " + str(location0))
        location1 = person1.getVisitLocationForDate(dateOfEvent)
        print(str(person1) + " " + str(location1))

        if ((location0==None) and (location1==None)):
            isPathCrossed = False
        elif(location0==location1):
            isPathCrossed = True
        return isPathCrossed
        

class CoronaTracker:
    
    listOfPeople = []

    @staticmethod
    def addPeople(person):
        CoronaTracker.listOfPeople.append(person)


    @staticmethod
    def reportSymptomEvent(person, year, month, day):
        person.hasSymptom(year, month, day)
        person.setIsolateCaution() #The Person who reports symptom should isolate
        print("----------")
        print(person)
        print("----------")
        dateOfSymptom = datetime.date(year, month, day)
        #Check if that person crossed path with other people. If they did, they should be careful
        for people in CoronaTracker.listOfPeople:
            
            if people!=person: #Only check the other people, not the reported person
                didPathCross = CrossPath.checkIfPathCrossed(person, people, dateOfSymptom)   
                print(didPathCross) 
                if(didPathCross==True):
                    print("This person came into contact: ")
                    print(people)
                    people.setCarefulCaution() #The people who crossed the path with the one who had symptom should be careful
                    didPathCross=False #Setting the flag to False 
    

    @staticmethod
    def reportAffectedEvent(person, year, month, day):
        person.hasSymptom(year, month, day)
        person.setIsolateCaution() #The Person who reports symptom should isolate
        print("----------")
        print(person)
        print("----------")
        dateOfSymptom = datetime.date(year, month, day)
        #Check if that person crossed path with other people. If they did, they should be careful
        for people in CoronaTracker.listOfPeople:
            
            if people!=person: #Only check the other people, not the reported person
                didPathCross = CrossPath.checkIfPathCrossed(person, people, dateOfSymptom)   
                print(didPathCross) 
                if(didPathCross==True):
                    print("This person came into contact: ")
                    print(people)
                    people.setIsolateCaution() #The people who crossed the path with the one who had symptom should be isolated
                    didPathCross=False #Setting the flag to False 







if __name__ == "__main__":

    A = Person()
    B = Person()
    C = Person()

    print(A)
    print(B)
    print(C)


    print("**********")
    visitDateA = datetime.date.today()
    location0 = Location(20.0, 21.0, 89.0, 89.1)
    A.visitsLocation(location0, visitDateA.year, visitDateA.month, visitDateA.day)
   

    B.visitsLocation(location0, visitDateA.year, visitDateA.month, visitDateA.day)
   
    print("**********")


    '''
    print(CrossPath.checkIfPathCrossed(A, B, visitDateA))
    print(CrossPath.checkIfPathCrossed(A, C, visitDateA))
    print(CrossPath.checkIfPathCrossed(B, C, visitDateA))
    '''

    
    CoronaTracker.addPeople(A)
    CoronaTracker.addPeople(B)
    CoronaTracker.addPeople(C)

    CoronaTracker.reportAffectedEvent(A, visitDateA.year, visitDateA.month, visitDateA.day)

    print("-----------------")
    print(A)
    print(B)
    print(C)
    
    
    '''
    symptomDateA = datetime.date.today()
    A.hasSymptom(symptomDateA.year, symptomDateA.month, symptomDateA.day)

    print(A)
    print(B)
    print(C)

    symptomDateB = datetime.date.today()
    A.isAffected(symptomDateB.year, symptomDateB.month, symptomDateB.day)

    print(A)
    print(B)
    print(C)
    '''