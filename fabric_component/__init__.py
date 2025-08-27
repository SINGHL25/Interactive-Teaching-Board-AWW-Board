
import streamlit.components.v1 as components

def st_fabric_board(key="fabric_board", width=800, height=600):
    # Embed Fabric.js canvas via HTML/JS
    component_value = components.html(f"""
        <canvas id="canvas" width="{width}" height="{height}" style="border:1px solid #000000;"></canvas>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.2.4/fabric.min.js"></script>
        <script>
            var canvas = new fabric.Canvas('canvas', {{ selection: true }});
            
            // Free drawing
            canvas.isDrawingMode = true;
            canvas.freeDrawingBrush.width = 5;
            canvas.freeDrawingBrush.color = '#000000';

            // Add text on double click
            canvas.on('mouse:dblclick', function(options) {{
                var text = new fabric.IText('Double-click to edit', {{
                    left: options.pointer.x,
                    top: options.pointer.y,
                    fill: '#FF0000',
                    fontSize: 24
                }});
                canvas.add(text);
                canvas.setActiveObject(text);
            }});
        </script>
    """, height=height)
    return component_value
