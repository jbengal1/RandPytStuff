import particles_manage
import run_manage

particles = particles_manage.Particles()
particles.initState1()

run = run_manage.Run()

run.run(particles)
run.plot()