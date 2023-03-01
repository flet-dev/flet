import multiprocessing
import random
import io
import mercantile
import urllib.request
import PIL.Image

def _download_tile(tile: mercantile.Tile):
    """
    Helper function for downloading associated image
    """
    server = random.choice(['a', 'b', 'c'])
    url = 'http://{server}.tile.openstreetmap.org/{zoom}/{x}/{y}.png'.format(
        server=server,
        zoom=tile.z,
        x=tile.x,
        y=tile.y
    )
    response = urllib.request.urlopen(url)
    img = PIL.Image.open(io.BytesIO(response.read()))

    return img, tile    

def get_image(west, south, east, north, zoom):
    """
    return glued tiles as PIL image
    :param west: west longitude in degrees
    :param south: south latitude in degrees
    :param east: east longitude in degrees
    :param north: north latitude in degrees
    :param zoom: wanted size
    :return: Image
    """
    tiles = list(mercantile.tiles(west, south, east, north, zoom))

    tile_size = 256
    min_x = min_y = max_x = max_y = None

    for tile in tiles:
        min_x = min(min_x, tile.x) if min_x is not None else tile.x
        min_y = min(min_y, tile.y) if min_y is not None else tile.y
        max_x = max(max_x, tile.x) if max_x is not None else tile.x
        max_y = max(max_y, tile.y) if max_y is not None else tile.y

    out_img = PIL.Image.new(
        'RGB',
        ((max_x - min_x + 1) * tile_size, (max_y - min_y + 1) * tile_size)
    )

    pool = multiprocessing.Pool(8)
    results = pool.map(_download_tile, tiles)
    pool.close()
    pool.join()

    for img, tile in results:
        left = tile.x - min_x
        top = tile.y - min_y
        bounds = (left * tile_size, top * tile_size, (left + 1) * tile_size, (top + 1) * tile_size)
        out_img.paste(img, bounds)

    return out_img   

if __name__ == '__main__':
    # get combined image and save to file
    get_image(west=103, south=51, east=110, north=56, zoom=8).save('osm_image.png')