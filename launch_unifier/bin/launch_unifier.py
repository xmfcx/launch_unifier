from pathlib import Path

from rclpy.logging import get_logger

from launch_unifier.filter import filter_entity_tree
from launch_unifier.parser import create_entity_tree
from launch_unifier.serialization import make_entity_tree_serializable

logger = get_logger("launch_unifier")


def _parse_args():
    import argparse

    import rclpy
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from ros2launch.command.launch import LaunchCommand

    rclpy.init()

    node = Node("launch2json")
    node.declare_parameter("launch_command", Parameter.Type.STRING)

    launch_command = node.get_parameter("launch_command")
    argv = launch_command.value.replace("ros2 launch ", "").split(" ")

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    LaunchCommand().add_arguments(parser, "ros2")

    rclpy.shutdown()

    return parser.parse_args(args=argv)


def main():
    args = _parse_args()

    import launch
    from ros2launch.api.api import get_share_file_path_from_package
    from ros2launch.api.api import parse_launch_arguments

    launch_file_path = get_share_file_path_from_package(
        package_name=args.package_name, file_name=args.launch_file_name
    )

    parsed_launch_arguments = parse_launch_arguments(args.launch_arguments)

    root_entity = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.AnyLaunchDescriptionSource(launch_file_path),
        launch_arguments=parsed_launch_arguments,
    )

    launch_service = launch.LaunchService(
        argv=parsed_launch_arguments, noninteractive=args.noninteractive, debug=args.debug
    )

    logger.info("Creating raw_tree...")
    raw_tree = create_entity_tree(root_entity, launch_service)
    logger.info("Created raw_tree")
    filtered_tree = filter_entity_tree(raw_tree.copy())

    logger.info("Creating serializable_tree")
    serializable_tree = make_entity_tree_serializable(filtered_tree, launch_service.context)
    logger.info("Created serializable_tree")

    from launch_unifier.launch_maker import generate_launch_file
    generated_launch_file = generate_launch_file(serializable_tree)
    logger.info("Generated the launch file")

    from launch_unifier.plantuml import generate_plantuml
    plantuml = generate_plantuml(serializable_tree)
    logger.info("Created plantuml")

    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "entity_tree.pu", "w") as f:
        f.write(plantuml)
    with open(output_dir / "generated.launch.xml", "w") as f:
        f.write(generated_launch_file)

    logger.info("Finished")

if __name__ == "__main__":
    main()
