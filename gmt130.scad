// Dimensions
pcb_width = 42.72;
pcb_height = 70.30;
pcb_thickness = 1.2;

pin_width = 17.78;
pin_height = 2.5;
pin_depth = 12.5;

screen_width = 37.42;
screen_height = 49.66;
screen_thickness = 1; // Assumed thickness
screen_offset_from_top = 15.3;

hole_diameter = 2.5;
hole_offset = 2.5;

// Main Assembly
module gmt130_display() {
    difference() {
        union() {
            // PCB
            pcb();

            // Pins on the back of the PCB
            pins();

            // Screen positioned from the top
            screen();
        }

        // Holes in the corners
        holes();
    }
}

// PCB Module
module pcb() {
    cube([pcb_width, pcb_height, pcb_thickness]);
}

// Pins Module
module pins() {
    pin_x_position = (pcb_width - pin_width) / 2;
    pin_y_position = 0; // Adjust if needed

    // Pins are on the back of the PCB (negative Z direction)
    translate([pin_x_position, pin_y_position, -pin_depth]) {
        cube([pin_width, pin_height, pin_depth]);
    }
}

// Screen Module
module screen() {
    x_position = (pcb_width - screen_width) / 2;
    y_position = pcb_height - screen_offset_from_top - screen_height;
    translate([x_position, y_position, pcb_thickness]) {
        cube([screen_width, screen_height, screen_thickness]);
    }
}

// Holes Module
module holes() {
    positions = [
        [hole_offset, hole_offset],
        [pcb_width - hole_offset, hole_offset],
        [hole_offset, pcb_height - hole_offset],
        [pcb_width - hole_offset, pcb_height - hole_offset]
    ];

    for (pos = positions) {
        translate([pos[0], pos[1], -1]) { // Extended into negative Z to ensure full cut-through
            cylinder(d = hole_diameter, h = pcb_thickness + 2 + pin_depth, $fn = 50);
        }
    }
}

// Render the GMT130 Display
gmt130_display();
