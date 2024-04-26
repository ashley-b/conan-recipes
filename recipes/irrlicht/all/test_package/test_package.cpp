#include <irrlicht.h>

using namespace irr;

using namespace core;
using namespace scene;
using namespace video;
using namespace io;
using namespace gui;

int main(int argc, char **argv)
{
  IrrlichtDevice *device =
      createDevice(video::EDT_NULL, dimension2d<u32>(640, 480), 16, false, false, false, 0);
  if (!device)
  {
    return 1;
  }

  device->setWindowCaption(L"Hello World! - Irrlicht Engine Demo");

  IVideoDriver *driver = device->getVideoDriver();
  ISceneManager *smgr = device->getSceneManager();
  IGUIEnvironment *guienv = device->getGUIEnvironment();

  guienv->addStaticText(L"Hello World! This is the Irrlicht Software renderer!", rect<s32>(10, 10, 260, 22), true);

  smgr->addCameraSceneNode(0, vector3df(0, 30, -40), vector3df(0, 5, 0));

  for (std::size_t i = 0; device->run(); i++)
  {
    driver->beginScene(true, true, SColor(255, 100, 101, 140));

    smgr->drawAll();
    guienv->drawAll();

    driver->endScene();
    if (i > 60)
    {
      device->closeDevice();
    }
  }

  device->drop();

  return 0;
}
