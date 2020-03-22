# Copyright 2019 DeepMind Technologies Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example use of the CFR algorithm on Kuhn Poker."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

from open_spiel.python.algorithms import cfr_full_rp_ave
from open_spiel.python.algorithms import exploitability
import pyspiel
import os
import numpy as np

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 201, "Number of iterations")
flags.DEFINE_string("game", "kuhn_poker", "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", 5, "How often to print the exploitability")


def main(_):
  game = pyspiel.load_game(FLAGS.game,
                           {"players": pyspiel.GameParameter(FLAGS.players)})
  cfr_solver = cfr_full_rp_ave.CFRSolver(game)

  path_name = "../data/cfr_full_rp_ave_{}/".format(FLAGS.game)
  if not os.path.exists(path_name):
      os.mkdir(path_name)
  file_name = path_name + "iter_{}_freq_{}_log.txt".format(FLAGS.iterations, FLAGS.print_freq)
  f = open(file_name, 'w')
  convs = []
  regs = []
  cfr_nodes = []

  for i in range(FLAGS.iterations):
    cfr_solver.evaluate_and_update_policy()
    if i % FLAGS.print_freq == 0:
      conv = exploitability.exploitability(game, cfr_solver.average_policy())
      reg = cfr_solver.get_regret()

      convs.append(conv)
      cfr_nodes.append(cfr_solver.nodes_touched)
      regs.append(reg)

      print("Iteration {} exploitability {}".format(i, conv))
      print("Current average regret {}".format(reg))
      print("Nodes touched {}".format(cfr_solver.nodes_touched))
      f.write("Iteration {} exploitability {}\n".format(i, conv))
      f.write("Current average regret {}\n".format(reg))
      f.write("Nodes touched{}\n".format(cfr_solver.nodes_touched))
  np.savez(path_name + "iter_{}_freq_{}.npz".format(FLAGS.iterations, FLAGS.print_freq), 
            convs=convs, cfr_nodes=cfr_nodes, regs=regs)
  f.close()

if __name__ == "__main__":
  app.run(main)
