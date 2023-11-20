import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Clase global para gestionar las piezas del juego y sus comportamientos."""

    def __init__(self):
        """Inicializamos el juego, y creamos sus recursos."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Inicia el circuito principal del juego."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(75)

    def _check_events(self):
        """Activa escucha de los eventos del mouse y teclado."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respuesta a las teclas oprimidas"""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_e:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respuesta a las teclas soltadas"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creamos una nueva bala y la agregamos al grupo de balas."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Actualizamos la posicion de las balas y eliminamos las que van
           saliendo de la pantalla."""
        # Actualizamos la posicion de las balas
        self.bullets.update()

        # Eliminamos las balas que ya han desaparecido, iterando sobre una copia
        # -de en este caso- grupo(pygame) de balas, y ya luego podemos modificar
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respuesta a la colision de alien-bala."""
        # Quitamos cualquier bala y alien hayan colisionado.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # Quitamos balas y hacemos otra flota
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Crea la flota de aliens."""
        # Hace un alien y sigue creando hasta que no haya espacio.
        # El espaciado entre alien es la anchura y altura del mismo.
        alien = Alien(self)
        # rect.size es un tupple con la anchura y altura.
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        # Determinamos si hay espacio, comparando el valor de current_x con el ancho
        # de la pantalla, asi como para current_y.
        # Agrega una nave si hay al menos 2 posibles espacios para naves
        # asi mantenemos el margen deseado a la derecha.
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finalizada una fila, reseteamos el valor de x, y incrementamos el de y.

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Crea un alien y lo coloca en la fila."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respondemos si cualquier alien llego a un borde."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Mueva abajo toda la flota y cambia la direccion de esta misma."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Chequea si un alien esta en el borde y actualizamos la posicion 
        de todos los aliens en la flota."""
        self._check_fleet_edges()
        self.aliens.update()

    def _update_screen(self):
        """Rehacemos la pantalla durante el paso cada loop."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Hace visible la pantalla mas reciente.
        pygame.display.flip()


if __name__ == '__main__':
    # Crea una instacia del juego, y la abre.
    ai = AlienInvasion()
    ai.run_game()
