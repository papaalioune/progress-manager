from __future__ import annotations
from abc import ABC, abstractmethod

class ProgressManagerAsSubject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """
    @abstractmethod
    def attach(self, observer: ProgressManagerAsObserver) -> None:
        """
        Attach an observer to the subject.
        """
        pass
    """
    @abstractmethod
    def attach_observers(self) -> None:
        pass
    """
    @abstractmethod
    def detach(self, observer: ProgressManagerAsObserver) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass

class ProgressManagerAsObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """ 
    @abstractmethod
    def update(self, subject: ProgressManagerAsSubject) -> None:
        """
        Receive update from subject.
        """
        pass    