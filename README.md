![Cover](https://hartface.github.io/images/AimingHelper/AimingHelperCover.png "Cover")

A Blender addon for visualizing and aligning sights on weapon models.
Useful for game asset artists who need to verify that eye, rear sight,
front sight and target are properly aligned.

## Installation

1. Download the latest release zip
2. In Blender go to **Edit → Preferences → Extensions → Install from Disk**
3. Select the zip and enable the addon

## Usage

Open the **N panel** in the 3D viewport and find the **Aiming Helper** tab.

1. Click **Pick** next to each point — Eye, Rear Sight, Front Sight, Target
2. Your cursor becomes an eyedropper — click directly on any mesh surface
3. The point anchors to that exact spot in local space, so it moves with the mesh
4. Hit **Start Visualizing** to see the alignment overlay
5. Adjust **Alignment Threshold** to control how strict the green/red check is

## What the overlay shows

- **Line** through all set points, green when aligned, red when not
- **Deviation lines** from each sight to where it should be on the ideal line
- **Angle readout** in degrees at each intermediate point
- **Status text** in the corner showing aligned/misaligned and exact deviation

## Notes

- You don't need all 4 points set to start visualizing, 2 is enough
- Points stick to whichever mesh surface you clicked, move the model and they follow
- Re-click Pick on any slot to reposition it

## Requirements

- Blender 4.2.0 or newer

## License

GPL-3.0-or-later
