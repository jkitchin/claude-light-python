"""An MCP server for Claude-Light.

Provides two tools for using Claude-Light from Claude-Desktop.

"""
from mcp.server.fastmcp import FastMCP
import requests
import json
import platform
import os
import shutil
import sys

# Initialize FastMCP server
mcp = FastMCP("claude-light")

@mcp.tool()
def about():
    """Describe Claude light."""
    return '''Claude-Light is a remote instrument that you use to do experiments
    with.

    Claude-light has an RGB LED with individually settable red, blue and green
    channels. There is a light sensor that reads the intensity at 8 different
    wavelengths (415nm, 445nm, 480nm, 515nm, 555nm, 590nm, 630nm, 680nm), and
    near-IR and a clear channel.

    You can learn more about it at
    https://github.com/jkitchin/claude-light?tab=readme-ov-file#claude-light
    '''


@mcp.tool()
def rgb(R: float, G: float, B: float) -> str:
    """Get output from Claude-Light.

    Args:
      R: the red channel setting, between 0 and 1.
      G: the green channel setting, between 0 and 1.
      B: the blue channel setting, between 0 and 1.

    Returns:

      The output of claude light in a dictionary. The "in" key contains the R,
    	G, B settings used. The "output" key contains the intensities in these
    	channels: 415nm, 445nm, 480nm, 515nm, 555nm, 590nm, 630nm, 680nm, clear,
    	nir

    """
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                        params={'R': R, 'G': G, 'B': B})

    d = resp.json()
    return d


def main():
    """Install, uninstall, or run the server.

    This is the cli. If you call it with install or uninstall as an argument, it
    will do that in the Claude Desktop. With no arguments it just runs the
    server.
    """

    if platform.system() == 'Darwin':
        cfgfile = '~/Library/Application Support/Claude/claude_desktop_config.json'
    elif platform.system() == 'Windows':
        cfgfile = r'%APPDATA%\Claude\claude_desktop_config.json'
    else:
        raise Exception('Only Mac and Windows are supported for the claude-light mcp server')

    cfgfile = os.path.expandvars(cfgfile)
    cfgfile = os.path.expanduser(cfgfile)

    with open(cfgfile, 'r') as f:
        cfg = json.loads(f.read())


    # Called with no arguments
    if len(sys.argv) == 1:
        mcp.run(transport='stdio')

    elif sys.argv[1] == 'install':

        setup = {"command": shutil.which("cl_mcp")}

        if "mcpServers" not in cfg:
            cfg["mcpServers"] = {}

        cfg["mcpServers"]["claude-light"] = setup
        with open(cfgfile, 'w') as f:
            f.write(json.dumps(cfg, indent=4))

        print(f'Installed claude-light. Here is your current {cfgfile}. Please restart Claude Desktop.')
        print(json.dumps(cfg, indent=4))

    elif sys.argv[1] == 'uninstall':
        if "mcpServers" not in cfg:
            cfg["mcpServers"] = {}

        if "claude-light" in cfg["mcpServers"]:
            del cfg["mcpServers"]["claude-light"]
            with open(cfgfile, 'w') as f:
                f.write(json.dumps(cfg, indent=4))

        print(f'Uninstalled claude-light. Here is your current {cfgfile}.')
        print(json.dumps(cfg, indent=4))

    else:
        print('I am not sure what you are trying to do. Please use install or uninstall.')
