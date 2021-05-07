# StopCorona API

Unofficial open public API for the info on https://stopcorona.tn.gov.in/, written in Python/Django.


## 🔎 Caveats and Considerations
* https://stopcorona.tn.gov.in/ is a public resource helping people in a time of need. Please be mindful of how often you make automated queries.
* The motivation behind this API is to provide a free, accessible, available API of COVID-19 facilities to enable others to build useful things that might help people.
* While this API is open to the public and free to use, I'm running it out of pocket. Please use it for something meaningful, and please be mindful of how much automated queries you send this way. 🙏
* Used this API to build something cool? I'd love to hear about it! Please tweet at 🐦 [@pradeepcep](https://twitter.com/pradeepcep) and let me know!


## 📝 Requirements
* Python 3.9.x
* Django 3.2.x
* Postgresql
* Git


## 👨‍💻 Development

1. `git clone` this repo.

2. Create a `.env` file and update the config:
```
cd stopcorona
cp .env.sample .env
vi .env
```

3. Install dependencies using `pipenv` (make sure you are using Python 3.9.x):
```
pipenv install --dev
pipenv shell
```

4. Run Django migrations, create a superuser, pull info to populate the database, and run the development server:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py pull_beds_info
python manage.py runserver
```

5. Report issues and raise pull requests for good karma! 🧘‍♂️


## 👨‍⚖️ License

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
