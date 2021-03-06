import os
import sys
from revolve.util import Supervisor
from online_evolve import parser

here = os.path.dirname(os.path.abspath(__file__))
tol_path = os.path.abspath(os.path.join(here, '..', '..'))
rv_path = os.path.abspath(os.path.join(tol_path, '..', 'revolve'))

args = parser.parse_args()

os.environ['GAZEBO_PLUGIN_PATH'] = os.path.join(tol_path, 'build')
os.environ['GAZEBO_MODEL_PATH'] = os.path.join(tol_path, 'tools', 'models')

supervisor = Supervisor(
    manager_cmd=[sys.executable, "online_evolve.py"],
    analyzer_cmd=os.path.join(rv_path, 'tools', 'analyzer', 'run-analyzer'),
    world_file=os.path.join(here, 'online-evolve.world'),
    output_directory=args.output_directory,
    manager_args=sys.argv[1:],
    restore_directory=args.restore_directory
)

supervisor.launch()
