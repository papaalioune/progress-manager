from abstract_progress_manager import ProgressManagerAsSubject as Subject, ProgressManagerAsObserver as Observer
from typing import List
#from time import sleep
import subprocess
from time import perf_counter

class GamaGeneralProgressManager(Subject):
    """
    Un objet de cette classe a un "nombre total de tâches" à superviser et un "nombre max de tâches par observer"
    à déleguer à ces derniers qu'ils doivent superviser et exécuter
    """
    def __init__(self, total_nb_tasks, max_nb_tasks_per_observer)-> None:
        super().__init__()
        self.total_nb_tasks = total_nb_tasks
        self.max_nb_tasks_per_observer = max_nb_tasks_per_observer
        self.observers: List[Observer] = []
        self.attach_observers()
        self.evolution = 0
    
    """
    Dans l'implémentation de ce "subject", il y'a deux types d'observers: les observers 
    (GamaTaskExecutionProgressManager) "exécutant" de tâche et un "observer" (ProgreesionViewer)
    visualisateur de l'évolution (progression) de l'exécution des tâches. Ces différents observers sont
    attachés au subjet au moment de sa construction.
    """

    def attach(self, observer: Observer) -> None:
        #print("Subject: Attached an observer.")
        self.observers.append(observer)

    """
    
    """
    def attach_observers(self) -> None:
        nbObservers = self.total_nb_tasks // self.max_nb_tasks_per_observer
        nbReste = self.total_nb_tasks % self.max_nb_tasks_per_observer
        for i in range(nbObservers):
            gepm = GamaTaskExecutionProgressManager(self.max_nb_tasks_per_observer)
            self.attach(gepm)
        if nbReste != 0:
            gepm = GamaTaskExecutionProgressManager(nbReste)
            self.attach(gepm)
        pv = ProgreesionViewer()
        self.attach(pv)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """
        for observer in self.observers:
            observer.update(self)

    def evolution_manage(self) -> None:
        """
        Cette méthode assure la gestion de la progression d'exécution des tâches     
        """
        start = perf_counter()
        while(self.evolution < self.total_nb_tasks):
            #Cette ligne permet de visualiser les observers à qui il reste des tâches à exécuter
            #print("Il me reste", len(self.observers) - 1, "exécutants de tâches")
            #tous les observers sont notifié pour renseigner sur l'évolution de leurs tâches respectives
            #(GamaTaskExecutionProgressManager) et pour visualiser l'évolution générale de l'exécution 
            #de toutes les tâches (observer ProgreesionViewer)
            self.notify()
            #sleep(1)
        #A ce stade, il ne reste plus que le viewer. Il est nitifié pour afficher le 100%
        self.notify()
        end = perf_counter()
        print(f"Fin des executions en {(end - start):.0f} secondes!\n")

    def afficher(self) -> None:
        print("I am a GAMA GENERAL MANAGER ... I have", len(self.observers),"observers")
        for a in self.observers:
            a.afficher()

class GamaTaskExecutionProgressManager(Observer):
    def __init__(self,  _nb_tasks) -> None:
        super().__init__()
        self._nb_tasks = _nb_tasks
        self.evolution = 0
        self.simulations_in_progress = False
        self.process = None

    def update(self, subject: GamaGeneralProgressManager) -> None:
        #Lancer la première tâche (subprocess)
        if (self.simulations_in_progress == False):
            self.process = subprocess.Popen(["python", "simulators.py"])
            self.simulations_in_progress = True
        #Renseigner l'evolution des tâches et lancement des tâches restantes
        if (self.evolution < self._nb_tasks):
            if self.process.poll() != None:
                #print("\nFin d'une simulation ...\n")
                self.evolution += 1
                subject.evolution += 1
                self.process = subprocess.Popen(["python", "simulators.py"])
        #Si toutes les tâches sont exécutées, l'observer se détache du subject pour ne plus être notifié
        if(self.evolution == self._nb_tasks):
            #print("I am finished-------")
            subject.detach(self)

    def afficher(self):
        print("I am a GAMA Task Execution manager ... I have ", self._nb_tasks, "tasks to manage")
        
class ProgreesionViewer(Observer):
    def update(self, subject: Subject) -> None:
        print(int((subject.evolution / subject.total_nb_tasks) * 100),"%")
        

    def afficher(self):
        print("I am a Progression Viewer")