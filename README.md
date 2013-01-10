Python HTN Planner
==================

The planner uses [SHOP algorithm](http://www.cs.umd.edu/projects/shop/description.html)

(the difference is that I don't support operators' add atoms and delete atoms lists)

Domains descriptions use Lisp's S-expressions similar to SHOP and JSHOP.

Planning domains are translated to Python code using planner compilation technique as in [JSHOP] (http://www.cs.umd.edu/projects/shop/).

Specific domain description language (methods and branches) is modelled after and influenced by [Guerrilla Games' presentation](http://www.guerrilla-games.com/presentations/GAIC09_Killzone2Bots_StraatmanChampandard.pdf) on their use of HTN.

The project is an experiment created for [AI Sandbox's](http://www.aisandbox.com) Capture The Flag Competition.

The code is in public domain.

You can find some very basic example domains under planner/examples directory.
