import numpy as np
from generator.GeneratorProblem import GeneratorProblem


class ManyObjectiveGenerator(GeneratorProblem):
    def __init__(self):
        super().__init__(
            n_var=10,
            n_obj=6,
            n_constr=1,
            #            type, dif, width, height, time, st_mg, hi_mg, tu_mp, ju_mp, cn_mp
            xl=np.array([0, 0, 149, 16, 30, -5, -5, 1, 1, 0]),
            xu=np.array([2, 15, 2 * 373, 2 * 16, 300, 5, 5, 5, 5, 10])
        )
        self.individuals = []

    def calc_results(self, result):
        return [
            result.getMarioNumHurts(),
            -result.getKillsTotal(),
            -(result.getNumJumps() + result.getMaxXJump() + result.getMaxJumpAirTime()),
            -result.getRemainingTime(),
            -(result.getNumCollectedMushrooms() + result.getNumCollectedFireflower() + result.getCurrentLives()),
            (result.getNumBumpQuestionBlock() + result.getNumBumpBrick() + result.getNumCollectedTileCoins() + result.getNumDestroyedBricks())
        ]

    def _evaluate(self, x, out, *args, **kwargs):
        results = []
        restrictions = []
        c = 0.2
        for [ty, d, w, h, ti, st_mg, hi_mg, tu_mp, ju_mp, cn_mp] in x:
            generator = ManyObjectiveGenerator.NotchGenerator(ty, d)
            level = generator.getGeneratedLevel(
                ManyObjectiveGenerator.MarioLevelModel(w, h),
                ManyObjectiveGenerator.MarioTimer(ti * 1000),
                st_mg, hi_mg, tu_mp, ju_mp, cn_mp
            )
            result = self.calc_results(
                ManyObjectiveGenerator.game.runGame(ManyObjectiveGenerator.agent, level, 20, 0, False))
            results.append(result)
            self.individuals.append({"result": result, "restriction": (c * w) - ti, "level": level})
            restrictions.append((c * w) - ti)
        out["F"] = np.array(results)
        out["G"] = np.array(restrictions)
