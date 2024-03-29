import numpy as np
from generator.GeneratorProblem import GeneratorProblem


class Ol2aGenerator(GeneratorProblem):
    def __init__(self, **kwargs):
        super().__init__(
            n_var=10,
            # n_obj=6,
            n_obj=3,
            n_constr=1,
            #            type, dif, width, height, time, st_mg, hi_mg, tu_mp, ju_mp, cn_mp
            xl=np.array([0, 0, 60, 16, 30, -5, -5, 1, 1, 0]),
            xu=np.array([2, 15, 120, 2 * 16, 300, 5, 5, 5, 5, 10]),
            **kwargs
        )
        self.individuals = []

    def calc_results(self, result):
        return np.array([
            #result.getMarioNumHurts(),
            -result.getKillsTotal(),
            -(result.getNumJumps() + result.getMaxXJump() + result.getMaxJumpAirTime()),
            -result.getRemainingTime(),
            # -(result.getNumCollectedMushrooms() + result.getNumCollectedFireflower() + result.getCurrentLives()),
            # (result.getNumBumpQuestionBlock() + result.getNumBumpBrick() + result.getNumCollectedTileCoins() + result.getNumDestroyedBricks())
        ])

    def _evaluate(self, x, out, *args, **kwargs):
        results = []
        restrictions = []
        c = 0.2
        for [ty, d, w, h, ti, st_mg, hi_mg, tu_mp, ju_mp, cn_mp] in [x]:
            generator = Ol2aGenerator.NotchGenerator(ty, d)
            level = generator.getGeneratedLevel(
                Ol2aGenerator.MarioLevelModel(w, h),
                Ol2aGenerator.MarioTimer(ti * 1000),
                st_mg, hi_mg, tu_mp, ju_mp, cn_mp
            )

            agent = Ol2aGenerator.RobinBaumgartenAgent()
            game = Ol2aGenerator.MarioGame()
            result = self.calc_results(game.runGame(agent, level, ti, 0, False))

            agent = Ol2aGenerator.SergeyPolikarpovAgent()
            game = Ol2aGenerator.MarioGame()
            result += self.calc_results(game.runGame(agent, level, ti, 0, False))

            agent = Ol2aGenerator.MichalAgent()
            game = Ol2aGenerator.MarioGame()
            result += self.calc_results(game.runGame(agent, level, ti, 0, False))

            result.__mul__(1/3)

            results.append(result)
            self.individuals.append({"result": result, "restriction": (c * w) - ti, "level": level})
            restrictions.append((c * w) - ti)
        out["F"] = result
        out["G"] = (c * w) - ti
