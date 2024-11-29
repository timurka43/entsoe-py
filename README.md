# entsoe-py

<!--- 
These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here  --->
![GitHub contributors](https://img.shields.io/github/contributors/timurka43/entsoe-py)
![GitHub stars](https://img.shields.io/github/stars/timurka43/entsoe-py?style=social)
![GitHub forks](https://img.shields.io/github/forks/timurka43/entsoe-py?style=social) 



*entsoe-py* is a tool that allows users to visualize EU electricity generation data aggregated from [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)

Current implementation supports manual specification of any region aggregated from the 27 EU countries, with the electricity generation data by source from 2015 onwards



## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have saved **your personal** key from ENTSO-E transparency platform in the *mykey.py* file in the repository.
* This is necessary if you want to occasionally update data with latest generation values by pulling directly from ENTSOE's RESTful API
* To obtain the key from ENTSO-E, follow [instructions here](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation)
* Once you have the key, define a ```get_key()``` function in *mykey.py* script to return your key as a string
* Place *mykey.py* in the *'entsoe-py/'* directory



## Using entsoe-py

To use entsoe-py:
* open main.ipynb in jupyter notebooks and follow the instructions



## Contributing to entsoe-py
<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->
To contribute to <project_name>, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

<!--- 
## Contributors

Thanks to the following people who have contributed to this project:

* [@scottydocs](https://github.com/scottydocs) 📖
* [@cainwatson](https://github.com/cainwatson) 🐛
* [@calchuchesta](https://github.com/calchuchesta) 🐛

You might want to consider using something like the [All Contributors](https://github.com/all-contributors/all-contributors) specification and its [emoji key](https://allcontributors.org/docs/en/emoji-key).
--->

## Acknowledgements

[@bfauser](github.com/bfauser/) : The base for this code was initially taken from [bfauser's entsoe-py](github.com/bfauser/entsoe-py) repository and further extensively updated and modified for my needs

## Contact

You can reach me at kasimovmoor [at] gmail [dot] com

## License
<!--- If you're not sure which open license to use see https://choosealicense.com/--->

This project is licensed under: [MIT License](https://github.com/timurka43/entsoe-py/blob/main/LICENSE).


