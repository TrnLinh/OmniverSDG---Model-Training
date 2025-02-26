import omni.replicator.core as rep
import random

with rep.new_layer():
    # Path to vegetation assets
    PROPS = 'C:/Users/local-lintran/Documents/Assets/Vegetation/Shrub/'
    # Path to car assets 
    CARS = "C:/Users/local-lintran/Desktop/cars"


    def random_props(size):
        # Create random car instances in the scene
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(CARS, recursive=True), size=size,
                                               mode='scene_instance')

        with instances:
            # Add semantic label for cars
            rep.modify.semantics([('class', "cars")])

            # Randomly position and rotate cars in the scene
            rep.modify.pose(
                position=rep.distribution.uniform((-1500, 0, -2000), (1500, 0, 1000)),
                rotation=rep.distribution.uniform((0, -180, 0), (0, 180, 0)),
            )

            # Randomize car colors
            rep.randomizer.color(colors=rep.distribution.uniform((0, 0, 0), (1, 1, 1)))
        return instances.node


    def get_props(size):
        # Create random vegetation instances
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(PROPS, recursive=True), size=size,
                                               mode='point_instance')

        with instances:
            # Randomly position and rotate vegetation
            rep.modify.pose(
                position=rep.distribution.uniform((-1500, 0, -2000), (1500, 0, 1000)),
                rotation=rep.distribution.uniform((-90, -180, 0), (-90, 180, 0)),

            )
        return instances.node


    # rep.randomizer.register(get_props)

    def dome_lights():
        # Create dome light with random HDR environment maps
        lights = rep.create.light(
            light_type="Dome",
            rotation=rep.distribution.uniform((0, 0, 0), (360, 0, 0)),
            texture=rep.distribution.choice([
                'C:/Users/local-lintran/Documents/Skies/Cloudy/champagne_castle_1_4k.hdr',
                'C:/Users/local-lintran/Documents/Skies/Clear/evening_road_01_4k.hdr',
                'C:/Users/local-lintran/Documents/Skies/Clear/mealie_road_4k.hdr',
                'C:/Users/local-lintran/Documents/Skies/Clear/qwantani_4k.hdr',
                "C:/Users/local-lintran/Documents/Skies/Evening/evening_road_01_4k.hdr",
                "C:/Users/local-lintran/Documents/Skies/Night/moonlit_golf_4k.hdr",
                "C:/Users/local-lintran/Documents/Skies/Night/kloppenheim_02_4k.hdr",

            ])
        )
        return lights.node


    # Create camera looking at scene center
    camera = rep.create.camera(position=(0, 1000, 2000), look_at=(0, 0, 0))

    # Create ground plane with PBR material
    ground_mat = rep.create.material_omnipbr(emissive_color=(.01, .01, .01), roughness=0.5, metallic=0.1, )
    ground = rep.create.plane(scale=1000, position=(0, 0, 0), material=ground_mat)

    with ground:
        # Add semantic label and physics for ground
        rep.modify.semantics([('class', "ground")])
        rep.physics.collider()

    # Set up render product with camera and resolution
    render_product = rep.create.render_product(camera, (1440, 1024))

    # Register randomizer functions
    rep.randomizer.register(get_props)
    rep.randomizer.register(random_props)
    rep.randomizer.register(dome_lights)

    print('triggering render')
    # Generate 1000 random scenes
    with rep.trigger.on_frame(max_execs=1000):
        rep.randomizer.random_props(5)  # Add 5 random cars
        rep.randomizer.get_props(20)    # Add 20 random vegetation props
        rep.randomizer.dome_lights()     # Add random lighting

    # Initialize and attach writer
    print('initializing writer')
    writer = rep.WriterRegistry.get('BasicWriter')
    output_dir = 'C:/Users/local-lintran/PycharmProjects/PythonProject3/data/new_data2'
    writer.initialize(
        output_dir=output_dir,
        rgb=True,
        bounding_box_2d_tight=True
    )
    writer.attach([render_product])

    # Run the orchestrator to generate dataset
    rep.orchestrator.run()

