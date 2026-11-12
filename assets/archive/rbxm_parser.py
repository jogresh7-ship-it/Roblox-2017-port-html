import struct
def lz4_block(src,usize):
  dst=bytearray();i=0;n=len(src)
  while i<n:
    t=src[i];i+=1;l=t>>4
    if l==15:
      while True:
        b=src[i];i+=1;l+=b
        if b!=255:break
    dst+=src[i:i+l];i+=l
    if i>=n:break
    off=src[i]|(src[i+1]<<8);i+=2;m=t&15
    if m==15:
      while True:
        b=src[i];i+=1;m+=b
        if b!=255:break
    m+=4;s=len(dst)-off
    for k in range(m):dst.append(dst[s+k])
  return bytes(dst)
def deinter(b,n,w):
  return [bytes(b[j*n+i] for j in range(w)) for i in range(n)]
def unzig(u):return (u>>1)^-(u&1)
def rfloat(b):
  u=struct.unpack('>I',b)[0];u=((u>>1)|((u&1)<<31))&0xffffffff;return struct.unpack('>f',struct.pack('>I',u))[0]
def ints(b,n):return [unzig(struct.unpack('>I',x)[0]) for x in deinter(b,n,4)]
def floats(b,n):return [rfloat(x) for x in deinter(b,n,4)]
def refs(b,n):
  v=ints(b,n);o=[];a=0
  for x in v:a+=x;o.append(a)
  return o
ROT={2:(1,0,0,0,1,0,0,0,1),3:(1,0,0,0,0,-1,0,1,0),5:(1,0,0,0,-1,0,0,0,-1),6:(1,0,0,0,0,1,0,-1,0),7:(0,1,0,1,0,0,0,0,-1),9:(0,0,1,1,0,0,0,1,0),10:(0,-1,0,1,0,0,0,0,1),12:(0,0,-1,1,0,0,0,-1,0),13:(0,1,0,0,0,1,1,0,0),14:(0,0,-1,0,1,0,1,0,0),16:(0,-1,0,0,0,-1,1,0,0),17:(0,0,1,0,-1,0,1,0,0),20:(-1,0,0,0,1,0,0,0,-1),21:(-1,0,0,0,0,1,0,1,0),23:(-1,0,0,0,-1,0,0,0,1),24:(-1,0,0,0,0,-1,0,-1,0),25:(0,1,0,-1,0,0,0,0,1),27:(0,0,-1,-1,0,0,0,1,0),28:(0,-1,0,-1,0,0,0,0,-1),30:(0,0,1,-1,0,0,0,-1,0),31:(0,1,0,0,0,-1,-1,0,0),33:(0,0,1,0,1,0,-1,0,0),34:(0,-1,0,0,0,1,-1,0,0),36:(0,0,-1,0,-1,0,-1,0,0)}
def parse(data):
  assert data[:8]==b'<roblox!'
  if data[14:16]!=b'\x00\x00':raise ValueError('ver')
  nclass,ninst=struct.unpack('<ii',data[16:24]);p=32;classes={};inst={};
  while p<len(data):
    name=data[p:p+4];cl,ul=struct.unpack('<II',data[p+4:p+12]);p+=16
    if cl:body=lz4_block(data[p:p+cl],ul);p+=cl
    else:body=data[p:p+ul];p+=ul
    if name==b'END\x00':break
    if name==b'INST':
      cid,sl=struct.unpack('<iI',body[:8]);cname=body[8:8+sl].decode('utf8','replace');q=8+sl+1;cnt=struct.unpack('<I',body[q:q+4])[0];q+=4
      rs=refs(body[q:q+cnt*4],cnt);classes[cid]={'name':cname,'refs':rs}
      for r in rs:inst[r]={'class':cname,'props':{},'parent':None}
    elif name==b'PROP':
      cid,sl=struct.unpack('<iI',body[:8]);pn=body[8:8+sl].decode('utf8','replace');q=8+sl;t=body[q];q+=1;d=body[q:]
      c=classes.get(cid);
      if not c:continue
      rs=c['refs'];n=len(rs);vals=None
      try:
        if t==1:
          vals=[];k=0
          for _ in range(n):L=struct.unpack('<I',d[k:k+4])[0];vals.append(d[k+4:k+4+L]);k+=4+L
        elif t==2:vals=[bool(x) for x in d[:n]]
        elif t==3:vals=ints(d,n)
        elif t==4:vals=floats(d,n)
        elif t==0x0B:vals=[struct.unpack('>I',x)[0] for x in deinter(d,n,4)]
        elif t==0x0E:vals=list(zip(floats(d[:4*n],n),floats(d[4*n:8*n],n),floats(d[8*n:12*n],n)))
        elif t==0x10:
          k=0;rots=[]
          for _ in range(n):
            rid=d[k];k+=1
            if rid==0:rots.append(struct.unpack('<9f',d[k:k+36]));k+=36
            else:rots.append(ROT.get(rid-1,(1,0,0,0,1,0,0,0,1)))
          pos=list(zip(floats(d[k:k+4*n],n),floats(d[k+4*n:k+8*n],n),floats(d[k+8*n:k+12*n],n)))
          vals=[(r,ps) for r,ps in zip(rots,pos)]
        elif t==0x12:vals=[struct.unpack('>I',x)[0] for x in deinter(d,n,4)]
        elif t==0x13:vals=refs(d,n)
        elif t==0x1A:vals=list(zip(d[:n],d[n:2*n],d[2*n:3*n]))
        elif t==0x0C:vals=list(zip(floats(d[:4*n],n),floats(d[4*n:8*n],n),floats(d[8*n:12*n],n)))
      except Exception as e:vals=None
      if vals is not None:
        for r,v in zip(rs,vals):inst[r]['props'][pn]=v
    elif name==b'PRNT':
      cnt=struct.unpack('<I',body[1:5])[0];ch=refs(body[5:5+4*cnt],cnt);pa=refs(body[5+4*cnt:5+8*cnt],cnt)
      for a,b in zip(ch,pa):
        if a in inst:inst[a]['parent']=b
  return inst
