import numpy as np
from generator.GeneratorProblem import GeneratorProblem


class MultiObjectiveGenerator(GeneratorProblem):
    def __init__(self):
        super().__init__(
            n_var=10,
            n_obj=2,
            n_constr=1,
            #            type, dif, width, height, time, st_mg, hi_mg, tu_mp, ju_mp, cn_mp
            xl=np.array([0, 0, 149, 16, 30, -5, -5, 1, 1, 0]),
            xu=np.array([2, 15, 2 * 373, 2 * 16, 300, 5, 5, 5, 5, 10])
        )
        self.individuals = []

    def calc_results(self, result):
        return [
            result.getMarioNumHurts() + result.getNumJumps(),  # min Dificuldade
            -(result.getKillsTotal() + result.getMaxXJump() + result.getMaxJumpAirTime())  # max Dificuldade
        ]

    def _evaluate(self, x, out, *args, **kwargs):
        results = []
        restrictions = []
        c = 0.2
        for [ty, d, w, h, ti, st_mg, hi_mg, tu_mp, ju_mp, cn_mp] in x:
            generator = MultiObjectiveGenerator.NotchGenerator(ty, d)
            level = generator.getGeneratedLevel(
                MultiObjectiveGenerator.MarioLevelModel(w, h),
                MultiObjectiveGenerator.MarioTimer(ti * 1000),
                st_mg, hi_mg, tu_mp, ju_mp, cn_mp
            )
            result = self.calc_results(
                MultiObjectiveGenerator.game.runGame(MultiObjectiveGenerator.agent, level, 20, 0, False))
            results.append(result)
            self.individuals.append({"result": result, "restriction": (c * w) - ti, "level": level})
            restrictions.append((c * w) - ti)
        out["F"] = np.array(results)
        out["G"] = np.array(restrictions)
