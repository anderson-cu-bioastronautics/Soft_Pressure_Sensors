clear
s = serial('COM12');
fopen(s);
z= 1;
t = 1;
while z==t
    fprintf(s, '%f', 1.5);
end

