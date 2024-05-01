# Actions

The actions are what actually do something with the files. There are a few default actions included in December, but you can also write your own.

## Writing your own actions

The file containing your action(s) needs to be in the `backend/actions` folder. The action class needs to inherit from `backend.actions.general_actions.Action`. It needs to have a doc string describing the action. The class variable `var_class` needs to be set to either the dataclass for the action's settings or to `None`. If the action requires settings, then make a class that inherits from `backend.actions.general_actions.ActionVars` and is also a dataclass. The `run` method receives the `files` variable which is a list of filenames and should return this list, potentially with changes depending on what the action does. You can not make an instance of the `backend.config.Config` class in the initialiser of the class; that has to be done in the `run` method instead. A template can be found below:

```python
#-*- coding: utf-8 -*-

"""
File: backend/actions/my_action.py
Action specifier: "my_action.MyAction"
"""

from dataclasses import dataclass

from backend.actions.general_actions import Action, ActionVars
from backend.config import Config

@dataclass
class MyActionVars(ActionVars):
	my_var: str
	"My description of my_var"

class MyAction(Action):
	"""
	My description of MyAction.
	"""
	
	var_class = MyActionVars
	
	def __init__(self, vars: MyActionVars) -> None:
		self.vars = vars
		return
	
	def run(self, files: List[str]) -> List[str]:
		self.config = Config().config
		
		# DO THIS AND THAT AND BOOM AND BAM
		
		return files
```
