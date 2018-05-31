import math

class polygon:

    def drawtile(canvas, tilevalue, tilesize, xpos, ypos):
        color_list = ['#EDE0C8',
            '#F3B179',
            '#F59563',
            '#ED785E',
            '#F55D3C',
            '#EDCE72',
            '#EDCB61',
            '#ECC750',
            '#EDC440',
            '#EDC12B',
            '#FF3D3B',
            '#FF1E1F',
            '#FF1E20',
            '#FF1E1F',
            '#FF1E1F',
            '#FF1E1E']
        if(tilevalue == 0):
            color_index = 0
        else:
            color_index = math.log(tilevalue, 2)
        canvas.create_rectangle(xpos, ypos, xpos+tilesize, ypos+tilesize, fill=color_list[int(color_index)])
        if(tilevalue != 0):
            canvas.create_text(xpos+tilesize/2, ypos+tilesize/2, text=tilevalue)
