 
## create some artists

`ar1 = Artist.objects.create(stage_name="Cairokee", social_media_link="https://www.instagram.com/cairokee/?hl=en")
  ar2 = Artist.objects.create(stage_name="Eminem", social_media_link="https://www.instagram.com/eminem/") 
  ar3 = Artist.objects.create(stage_name="Frank Sinatra", social_media_link="https://www.instagram.com/sinatra/?hl=en") 
  ar4 = Artist.objects.create(stage_name="Drake", social_media_link="https://www.instagram.com/champagnepapi/?hl=en")` 
  
## list down all artists
Artist.objects.all()
>>> <QuerySet [<Artist: Adele>, <Artist: Cairokee>, <Artist: Drake>, <Artist: Eminem>, <Artist: Frank Sinatra>]>

## list down all artists Sorted by name
Artist.objects.all().order_by("stage_name") 
>>> <QuerySet [<Artist: Adele>, <Artist: Cairokee>, <Artist: Drake>, <Artist: Eminem>, <Artist: Frank Sinatra>]>

## list down all artists whose name starts with 'a'
Artist.objects.filter(stage_name__startswith='a')
>>> <QuerySet [<Artist: Adele>]>

## in 2 different ways, create some albums and assign them to any artists 

### 1
dt = datetime(2017,7,20, 1,0,0)
dt = dt.replace(tzinfo=timezone.utc)
album1 = Album.objects.create(album_name="Noata Beda",album_release_date=dt, artist=ar1, cost=49.99)
album1
>>> <Album: Noata Beda>

dt = datetime(2000,5,23, 0,0,0)
dt = dt.replace(tzinfo=timezone.utc)
ar2 = Artist.objects.get(stage_name="Eminem")
album2 = Album.objects.create(album_name="The Marshall Mathers LP",album_release_date=dt, artist=ar2, cost=49.99)
album2
>>> <Album: The Marshall Mathers LP>

### 2
dt = datetime(2022,9,29, 0,0,0)
dt = dt.replace(tzinfo=timezone.utc)
album3 = Album()
album3.album_name = "Roma"
album3.album_release_date = dt
album3.artist = ar1
album3.cost = 49.99
album3.save()
album3
>>> <Album: Roma>


## Latest released albums
>>> latest_date = Album.objects.aggregate(latest = Max('album_release_date'))
>>> latest_date
{'latest': datetime.datetime(2022, 9, 29, 0, 0, tzinfo=datetime.timezone.utc)}
>>> Album.objects.filter(album_release_date=latest_date['latest'])
<QuerySet [<Album: Roma>]>


## Albums Released Before today
>>> today = timezone.now()
>>> Album.objects.filter(album_release_date__lt=today)
<QuerySet [<Album: Noata Beda>, <Album: The Marshall Mathers LP>, <Album: Roma>]>



## Albums Released today or Before but not after
>>> today = timezone.now()
>>> Album.objects.filter(album_release_date__lte=today)
<QuerySet [<Album: Noata Beda>, <Album: The Marshall Mathers LP>, <Album: Roma>]>


## Count the total number of albums
>>> Album.objects.count()
3

## Get All albums of artists
1 : 
>>> ar1.albums.all()
<QuerySet [<Album: Noata Beda>, <Album: Roma>]>
>>> ar2.albums.all()
<QuerySet [<Album: The Marshall Mathers LP>]>

2 : 
Artist.objects.get(stage_name="Cairokee").albums.all()
<QuerySet [<Album: Noata Beda>, <Album: Roma>]>
>>> Artist.objects.get(stage_name="Eminem").albums.all()
<QuerySet [<Album: The Marshall Mathers LP>]>


## Order by Cost then Album Name
Album.objects.all().order_by("cost","album_name")
<QuerySet [<Album: Noata Beda>, <Album: Roma>, <Album: The Marshall Mathers LP>]>


## Order Artists according to Number of Approved albums
>>> Artist.objects.all().annotate(approved_albums=Count('albums__approved')).order_by('-approved_albums')
<QuerySet [<Artist: Cairokee>, <Artist: Eminem>, <Artist: Adele>, <Artist: Drake>, <Artist: Frank Sinatra>]>




