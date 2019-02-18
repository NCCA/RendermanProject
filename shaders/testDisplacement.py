#!/usr/bin/python
from __future__ import print_function
import prman
import sys,os.path,subprocess
sys.path.append('../python')
import ProcessCommandLine as cl

# Main rendering routine
def main(filename,shadingrate=10,pixelvar=0.1,
         fov=45.0,width=1024,height=720,
         integrator='PxrPathTracer',integratorParams={}
        ) :
  print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
  ri = prman.Ri() # create an instance of the RenderMan interface

  # this is the begining of the rib archive generation we can only
  # make RI calls after this function else we get a core dump
  ri.Begin(filename)
  ri.Option('searchpath', {'string archive':'./:@'})
  ri.Option('searchpath', {'string texture':'../sourceImages/:@'})

  # now we add the display element using the usual elements
  # FILENAME DISPLAY Type Output format
  ri.Display('ferry.exr', 'it', 'rgba')
  ri.Format(width,height,1)

  # setup the raytrace / integrators
  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  #ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })
  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})

  #ri.Rotate(12,1,0,0)
  ri.Translate( 0, 0 ,2.5)


  # now we start our world
  ri.WorldBegin()



  #######################################################################
  #Lighting We need geo to emit light
  #######################################################################
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)
  ri.Rotate(180,0,0,1)
  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'lightMap.tex'
   })
  ri.TransformEnd()
  #######################################################################
  # end lighting
  #######################################################################

  ri.AttributeBegin()

  ri.Attribute ('trace' ,{'int displacements' : [ 1 ], "int autobias" : [1] ,"float bias" : [0.1]})
  
  ri.Attribute ('displacementbound', {'float sphere' : [2], 'string coordinatesystem' : ['object']})

  ri.Pattern('rustDisplace','rustDisplace', 
  { 
    'float dispScale' : [0.015],
    'float spread' : [12.638],
    'float pointSpreadX' : [510.0],
    'float pointSpreadY' : [210.0],
     
  })
  
  
  
  
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [1.0],
    'reference float dispScalar' : ['rustDisplace:resultF'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["mainplate"]
  })

  ri.Attribute( 'user' , {'string __materialid' : ['mainplate'] })
  plate=ri.ObjectBegin()
  # ri.Polygon({ 'P' : [-1 , 1 , 0, 
  #                      1 , 1 , 0, 
  #                      1,  -1.4 , 0, 
  #                     -1,  -1.4 , 0
  #                     ]})
  ri.HierarchicalSubdivisionMesh("catmull-clark" ,[4 ,4 ,4 ,4, 4 ,4 ,4 ,4 ,4], 
    [4, 5, 1, 0, 5, 6, 2, 1, 6, 7, 3, 2, 8 ,9, 5, 4, 9 ,10 ,6 ,5 ,10, 11, 7, 6, 12, 13, 9 ,8 ,13, 14, 10, 9, 14, 15, 11, 10], 
    ["interpolateboundary"] ,[1 ,0 ,0] ,[2] ,[] ,[], 
    {"P"  : [-1, -1, 0 ,-0.333333, -1, 0 ,0.333333, -1, 0, 1 ,-1, 0,      -1 ,-0.333333 ,0, -0.333333, -0.333333 ,0 ,0.333333 ,-0.333333, 0, 1, -0.333333 ,0,
      -1, 0.333333 ,0, -0.333333 ,0.333333, 0, 0.333333, 0.333333 ,0, 1, 0.333333, 0,
      -1, 1, 0, -0.333333, 1 ,0 ,0.333333, 1, 0 ,1 ,1, 0,]} )

  


  ri.ObjectEnd()
  ri.Bxdf ('PxrSurface' , 'mainplate', 
  {
    'color diffuseColor' : [0.6,0.6,0.6] ,
    'string __materialid' : ['mainplate']  
  })
  
  

  # top left front  
  ri.TransformBegin()
  ri.Scale(0.5,0.5,0.5)
  ri.Translate(-1,1.2,0)
  ri.ObjectInstance(plate)

  ri.TransformEnd()
  # top right flat 45
  ri.TransformBegin()
  ri.Scale(0.5,0.5,0.5)
  ri.Translate(1,1.2,0)
  ri.Rotate(45,1,0,0)
  ri.ObjectInstance(plate)
  ri.TransformEnd()
  # bottom left  
  ri.TransformBegin()
  ri.Scale(0.5,0.5,0.5)
  ri.Translate(-1,-1.2,0)
  ri.Rotate(35,0,1,0)
  ri.ObjectInstance(plate)

  ri.TransformEnd()
  # bottom right
  ri.TransformBegin()
  ri.Scale(0.5,0.5,0.5)
  ri.Translate(1,-1.2,0)
  ri.Rotate(-25,0,1,0)
  ri.ObjectInstance(plate)

  ri.TransformEnd()
  

  ri.AttributeEnd()
  
  # end our world
  ri.WorldEnd()
  # and finally end the rib file
  ri.End()


'''
function to check if shader exists and compile it, we assume that the shader
is .osl and the compiled shader is .oso If the shader source is newer than the
compiled shader we will compile it. It also assumes that oslc is in the path.
'''
def checkAndCompileShader(shader) :
	if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
		print( 'compiling shader {0}'.format(shader))
		try :
			subprocess.check_call(['oslc', shader+'.osl'])
		except subprocess.CalledProcessError :
			sys.exit('shader compilation failed')
		 

if __name__ == '__main__':  
  shaderName='rustDisplace'
  checkAndCompileShader(shaderName)
  cl.ProcessCommandLine('testDisplacement.rib')
  main(cl.filename,cl.args.shadingrate,cl.args.pixelvar,cl.args.fov,cl.args.width,cl.args.height,cl.integrator,cl.integratorParams)

