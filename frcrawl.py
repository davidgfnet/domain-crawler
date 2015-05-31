#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import string, sys

extensions = ["fr", "pm", "re", "tf", "wf", "yt"]

im = Image.open(sys.argv[1]).convert('RGB')

patterns = {}
for l in list(string.ascii_lowercase) + ["é","è","-"] + [str(x) for x in range(10)]:
  try:
    pp = Image.open("font/bin/" + l + ".png").convert('RGB')
    if pp.size[1] == 16:
      patterns[l] = pp
  except:
    pass

#print patterns.keys()

def lum((r,g,b)): return 0.2126*r + 0.7152*g + 0.0722*b

def get_err(im1, im2):
  assert im1.size == im2.size
  err = 0
  for i in range(im1.size[0]):
    for j in range(im1.size[1]):
      l1 = lum(im1.getpixel((i,j)))
      l2 = lum(im2.getpixel((i,j)))
      perr = abs(l1-l2)/256
      err += perr
  return err/im1.size[0]/im1.size[1]

class BM():
  def __init__(self, s):
    self._bm = [False]*s
  def set(self, xcoord, size):
    for i in range(xcoord, xcoord+size):
      self._bm[i] = True
  def check(self, xcoord, size, maxoverlap):
    if xcoord + size >= len(self._bm): return False
    for i in range(xcoord+maxoverlap, xcoord+size-maxoverlap):
      if self._bm[i]:
        return False
    return True
  def __str__(self):
    return "".join([ "1" if x else "0" for x in self._bm])

def brute(im, pat):
  # Create a bitmap
  rawlist = []

  # For every Y position
  for i in range(im.size[0]):
    # For every possible letter
    icoord = {}
    for p in pat:
      # Calculate the color error
      block = im.crop((i, 0, i+pat[p].size[0], 16))
      err = get_err(block, pat[p])
      # No error, inmediate assign!
      icoord[p] = err
      #print i, p, err

    rawlist.append(icoord)

  bm = BM(im.size[0])
  llist = {}
  # First pass, exact matchs
  for i,coord in enumerate(rawlist):
    for p in coord:
      if coord[p] == 0:
        if bm.check(i, pat[p].size[0], 0):
          bm.set(i, pat[p].size[0])
          llist[i] = p
  # Second pass, best match that doesn't overlap
  #for i,coord in enumerate(rawlist):
  for i,coord in enumerate(rawlist):
    for p in sorted(coord, key=coord.get):
      if coord[p] < 0.06:
        if bm.check(i, pat[p].size[0], 0):
          llist[i] = p
          bm.set(i, pat[p].size[0])

  return "".join([x[1] for x in sorted(list(llist.items()))])

header_ends = 292

header = im.crop((0, 0, im.size[0], header_ends))
body   = im.crop((0, header_ends, im.size[0], im.size[1]))

def remwhite(im):
  start = 0
  end = im.size[0]
  for i in range(im.size[0]):
    allwhite = True
    for j in range(im.size[1]):
      if lum(im.getpixel((i,j))) < 250:
        allwhite = False
        break
    if allwhite: start += 1
    else: break

  for i in range(im.size[0]-1, 0, -1):
    allwhite = True
    for j in range(im.size[1]):
      if lum(im.getpixel((i,j))) < 250:
        allwhite = False
        break
    if allwhite: end -= 1
    else: break

  return im.crop((start, 0, end, 16))

numd = 1
c = 0
for i in range(16*numd, body.size[1], 16*numd):
  chunk = body.crop((0,i, body.size[0], i+16*numd))
  chunk = remwhite(chunk)
  c += 1

  # Bruteforce OCR
  word = brute(chunk, patterns)
  for ext in extensions:
    if word.endswith(ext): word = word[:-len(ext)] + "." + ext
    break

  #chunk.save("out/%s.png"%word)
  print word


