import sys
import random
import argparse
import datetime
import pathlib

import yaml


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("config_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)

    options = parser.parse_args()

    config = read_config(options.config_file)
    draw_partners(config)


def read_config(config_file):
    config = yaml.safe_load(config_file)
    return Configuration(config)


class Configuration(object):
    def __init__(self, config):
        self.config = config
        self.person_info = config['persons']
        self.persons = set(self.person_info.keys())
        self.settings = config['settings']
        self.draw_settings = self.settings.setdefault('draw', {})
        self.email_settings = self.settings.setdefault('email', {})
        self.site_settings = self.settings.setdefault('site', {})
        self.history = config.setdefault('history', {})
        self.exclusions = self._build_exclusions(config)

    def get_person(self, key):
        return self.person_info.get(key)

    def append_to_history(self, partners):
        self.history[datetime.date.today()] = partners

    def save_with_timestamp(self, path):
        path = pathlib.Path(path)
        name = "%s-%s" % (datetime.date.today().isoformat(), path.name)
        with open(str(path.parent / name), "w+") as f:
            yaml.safe_dump(self.config, f, default_flow_style=False)

    def _build_exclusions(self, config):
        exclusions = set()

        for exclusion in config.get('exclusions', ()):
            for giver in exclusion:
                for receiver in exclusion:
                    if giver != receiver:
                        exclusions.add((giver, receiver))
                        exclusions.add((receiver, giver))

        history_count = self.draw_settings.get('avoid_previous_partners', 0)

        history = [
            assignments for date, assignments in
            sorted(self.history.items(), key=lambda e: e[0], reverse=True)
        ][:history_count]

        exclusions |= set(
            tuple(assignment)
            for assignments in history
            for assignment in assignments.items()
        )

        print("Exclusions:")
        for giver, receiver in exclusions:
            print(giver + " -> " + receiver)
        print()

        return exclusions


def draw_partners(config):
    givers = list(config.persons)
    random.shuffle(givers)
    receivers = set(config.persons)
    partners = {}

    print("Draw:")
    if not draw_next_partner(givers, receivers, partners, config):
        raise Exception("No possible solution found")

    print("\nMatch up:")
    for giver, receiver in partners.items():
        print(giver + " -> " + receiver)

    return partners


def draw_next_partner(givers, receivers, partners, config, level=0):
    if not givers:
        return True

    giver = givers.pop()
    possible_receivers = list(receivers)
    random.shuffle(possible_receivers)

    for receiver in possible_receivers:
        if receiver == giver:
            continue

        print(" " * level + giver + " -> " + receiver)

        partners[giver] = receiver

        if not is_valid_match_up(partners, config):
            continue

        receivers.remove(receiver)

        if draw_next_partner(givers, receivers, partners, config, level + 1):
            return True

        receivers.add(receiver)

    givers.append(giver)

    if giver in partners:
        partners.pop(giver)

    return False


def is_valid_match_up(partners, config):
    for giver, receiver in partners.items():
        if giver == receiver or (giver, receiver) in config.exclusions:
            return False

    min_circle_size = config.draw_settings.get('min_circle_size')
    if min_circle_size:
        remaining = set(config.persons)
        while remaining:
            circle_size = 0
            first_person = current_person = remaining.pop()

            while current_person is not None:
                if current_person in remaining:
                    remaining.remove(current_person)

                circle_size += 1
                current_person = partners.get(current_person)

                if current_person == first_person:
                    if circle_size < min_circle_size:
                        return False
                    break

    return True


if __name__ == "__main__":
    main()
