from pymoo.core.problem import Problem
from pymoo.core.problem import ElementwiseProblem

import jnius_config
jnius_config.add_classpath("/media/peixoto/Data/TCC/Mario-AI-Framework/out/artifacts/Mario_AI_Framework_jar/*")

from jnius import autoclass

class GeneratorProblem(ElementwiseProblem):
    MarioLevelModel = autoclass('marioai.engine.core.MarioLevelModel')
    MarioTimer = autoclass('marioai.engine.core.MarioTimer')
    PlayLevel = autoclass('marioai.PlayLevel')
    MarioGame = autoclass('marioai.engine.core.MarioGame')
    MarioLevelGenerator = autoclass('marioai.engine.core.MarioLevelGenerator')
    NotchGenerator = autoclass('marioai.levelGenerators.notch.LevelGenerator')
    MarioResult = autoclass('marioai.engine.core.MarioResult')
    SergeyPolikarpovAgent = autoclass('marioai.agents.sergeyPolikarpov.Agent')
    RobinBaumgartenAgent = autoclass('marioai.agents.robinBaumgarten.Agent')
    TrondEllingsenAgent = autoclass('marioai.agents.trondEllingsen.Agent')
    MichalAgent = autoclass('marioai.agents.michal.Agent')
