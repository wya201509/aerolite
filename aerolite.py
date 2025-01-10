import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation # 导入模块

class Sand:
    def __init__(self, x, y, z, vx, vy, vz, m, ty, temp):
        self.x = x
        self.y = y
        self.z = z # 位置
        self.vx = vx
        self.vy = vy
        self.vz = vz # 速度
        self.m = m # 质量
        self.ty = ty # 类型
        self.temp = temp # 温度
        
    def update(self, g, dt):
        ax = 0.0
        ay = 0.0
        az = 0.0 - g # 加速度
        for other in sands: # 遍历
            if other is not self:
                if self.ty == 'sand':
                    dx = other.x - self.x
                    dy = other.y - self.y
                    dz = other.z - self.z # 位置差
                    dist = np.sqrt(dx**2+dy**2+dz**2) # 勾股定理，+1防止/0
                    if dist < 3: # 检测碰撞
                        # 计算加速度
                        ax += other.vx * np.sqrt(other.vx**2) * other.m / (2 * self.m)
                        ay += other.vy * np.sqrt(other.vy**2) * other.m / (2 * self.m)
                        az += other.vz * np.sqrt(other.vz**2) * other.m / (2 * self.m)
                        self.temp = (self.temp + other.temp) / 2
                        other.temp = self.temp # 计算温度
                    
        self.vx += ax * dt
        self.vy += ay * dt
        self.vz += az * dt # 计算速度
        inScreen = \
        -400 < self.x + self.vx * dt < 400 and \
                -400 < self.y + self.vy * dt < 400 and \
                -400 < self.z + self.vz * dt < 400 # 检测是否碰到屏幕边缘
        if inScreen:
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.z += self.vz * dt # 计算位置
        self.temp -= 10 * dt

def create_colorbar():
    # 创建ScalarMappable对象，用于将温度映射到颜色
    temp_min = 0
    temp_max = 2550
    norm = plt.Normalize(vmin=temp_min, vmax=temp_max)
    sm = plt.cm.ScalarMappable(cmap='rainbow', norm=norm)
    sm.set_array([])  # 初始化为空数组，稍后会为每个沙粒设置颜色

    # 添加颜色条
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label('Temperature')

def update_figure(j):
    global i
    dt = 0.1 # 时间间隔
    for sand in sands:
        sand.update(g, dt)
    print(f"Round {i}")
    
    ax.clear()

    # 绘制散点图，并使用温度作为颜色
    temp_min = 0
    temp_max = 2550
    norm = plt.Normalize(vmin=temp_min, vmax=temp_max)
    sm = plt.cm.ScalarMappable(cmap='rainbow', norm=norm)
    scatter = ax.scatter(
        [sand.x for sand in sands],
        [sand.y for sand in sands],
        [sand.z for sand in sands],
        s=[sand.m ** (1/3) for sand in sands],  
        c=[sm.to_rgba(sand.temp) for sand in sands],
    )
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    ax.set_zlim(-400, 400)
    
    plt.pause(0.01)
    if i % 10 == 0:
        plt.savefig(f'{i}.png', bbox_inches='tight')
    i += 1

sands = []
g = 9.8 # 重力加速度

m = 4000
ty = 'aerolite'
temp = 2500
x, y, z, vx, vy, vz = 0, 0, 0, 0, 0, 0 - g
s = Sand(x, y, z, vx, vy, vz, m, ty, temp)
sands.append(s)
for i in range(800):
    m = np.random.uniform(0.3, 1.3)
    ty = 'sand'
    temp = np.random.uniform(0.3, 1.3)
    x, y = np.random.uniform(-400, 400, size=2)
    z = np.random.uniform(-400, -370)
    vx, vy, vz = 0, 0, 0
    s = Sand(x, y, z, vx, vy, vz, m, ty, temp)
    sands.append(s)

i = 1
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

create_colorbar()
ani = FuncAnimation(fig, update_figure, frames=range(50), interval=100)
plt.show()
