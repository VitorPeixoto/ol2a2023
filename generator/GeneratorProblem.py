from pymoo.core.problem import Problem

import jnius_config
jnius_config.add_classpath("/home/peixoto/Documentos/tcc/Mario-AI-Framework/out/artifacts/Mario_AI_Framework_jar/*")

from jnius import autoclass

class GeneratorProblem(Problem):
    MarioLevelModel = autoclass('marioai.engine.core.MarioLevelModel')
    MarioTimer = autoclass('marioai.engine.core.MarioTimer')
    PlayLevel = autoclass('marioai.PlayLevel')
    MarioGame = autoclass('marioai.engine.core.MarioGame')
    MarioLevelGenerator = autoclass('marioai.engine.core.MarioLevelGenerator')
    NotchGenerator = autoclass('marioai.levelGenerators.notch.LevelGenerator')
    MarioResult = autoclass('marioai.engine.core.MarioResult')
    RobinBaumgartenAgent = autoclass('marioai.agents.robinBaumgarten.Agent')
    game = MarioGame()
    agent = RobinBaumgartenAgent()
