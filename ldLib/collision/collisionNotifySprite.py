__author__ = 'Bobsleigh'

from collision.collisionTile import *

def collisionNotifySprite(sprite, tileType, mapData):
    tile, direction = rightCollision(sprite, tileType, mapData)
    if tile != NONE:
        sprite.onCollision(tile, direction)
    tile, direction = leftCollision(sprite, tileType, mapData)
    if tile != NONE:
        sprite.onCollision(tile, direction)
    tile, direction = downCollision(sprite, tileType, mapData)
    if tile != NONE:
        sprite.onCollision(tile, direction)
    tile, direction = upCollision(sprite, tileType, mapData)
    if tile != NONE:
        sprite.onCollision(tile, direction)